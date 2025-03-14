
import os
from dotenv import load_dotenv
import sys
import time
import asyncio
import argparse

import runpod
from runpod import RunPodLogger
from runpod.serverless.modules import rp_http


MOCK_RETURN_DEFAULT = os.environ.get('MOCK_RETURN', [
            'a beautiful high resolution image of the sunset',
            'a beautiful abstract drawing of the sunset in pastel colors',
            'a beautiful, award-winning image of the sunset over rolling green hills',
            'a masterpiece painting of the sunset over green hillsides. vibrant colors',
        ]
    )
MOCK_DELAY_DEFAULT = os.environ.get('MOCK_DELAY', 1)
MOCK_PROGRESS_DEFAULT = os.environ.get('MOCK_PROGRESS', [
            'Phase 1/4: SD initializing (MOCK)',
            'Phase 2/4: CLIP encoder running (MOCK)',
            'Phase 3/4: Diffusion model running (MOCK)',
            'Phase 4/4: VAE generating image',
        ]
    )
MOCK_ERROR_DEFAULT = os.environ.get('MOCK_ERROR', False)
MOCK_CRASH_DEFAULT = os.environ.get('MOCK_CRASH', False)
MOCK_REFRESH_DEFAULT = os.environ.get('MOCK_REFRESH', False)

MOCK_EXTERNAL_DEFAULT = os.environ.get('MOCK_EXTERNAL', {})


log = RunPodLogger()


def concurrency_modifier(current_concurrency=1):
    """ Returns the concurrency modifier for the worker. """
    return int(os.environ.get('CONCURRENCY_MODIFIER', current_concurrency))


# ----------------------------- Standard Handler ----------------------------- #
def handler(job):
    '''
    The handler function that will be called by the serverless.
    '''
    print(f"mock-worker | Starting job {job['id']}")

    job_input = _side_effects(job)

    time.sleep(job_input.get('mock_delay', MOCK_DELAY_DEFAULT))

    # Prepare the job output
    job_output = job_input.get('mock_return', 'Hello World!')

    # Mock enabled refresh_worker
    if job_input.get('mock_refresh', MOCK_REFRESH_DEFAULT):
        job_output = {
            'refresh_worker': True,
            'mock_return': job_output
        }

    # Mock job progress updates
    if job_input.get('mock_progress', MOCK_PROGRESS_DEFAULT):
        for update in job_input['mock_progress'].get('updates', []):
            runpod.serverless.progress_update(job, update)
            time.sleep(job_input['mock_progress'].get('wait_time', 0))

    # Mock the job returning a value
    return job_output


# ----------------------------- Generator handler ---------------------------- #
def generator_handler(job):
    '''
    Generator type handler.
    '''
    job_input = _side_effects(job)

    # Prepare the job output
    job_output = job_input.get('mock_return', MOCK_RETURN_DEFAULT)

    for output in job_output:
        time.sleep(job_input.get('mock_delay', MOCK_DELAY_DEFAULT))
        yield output


async def async_generator_handler(job):
    '''
    Async generator type handler.
    '''
    job_input = _side_effects(job)

    # Prepare the job output
    job_output = job_input.get('mock_return', MOCK_RETURN_DEFAULT)
    print("DEBUG:")
    print(job_output)

    for output in job_output:
        await asyncio.sleep(job_input.get('mock_delay', MOCK_DELAY_DEFAULT))
        yield output


# ------------------------------- Side Effects ------------------------------- #
def _side_effects(job):
    '''
    Modify the behavior of the handler based on the job input.
    '''
    job_input = job['input']

    # Mock json logs
    for job_log in job_input.get('mock_logs', []):
        log_level = job_log.get('level', "info").lower()

        if log_level == 'debug':
            log.info(job_log['message'], job_id=job['id'])
        elif log_level == 'info':
            log.info(job_log['message'], job_id=job['id'])
        elif log_level == 'warn':
            log.warn(job_log['message'], job_id=job['id'])
        elif log_level == 'error':
            log.error(job_log['message'], job_id=job['id'])

    # Mock the job crashing the worker
    if job_input.get('mock_crash', MOCK_CRASH_DEFAULT):
        os._exit(1)

    # Mock the job throwing an exception
    if job_input.get('mock_error', MOCK_ERROR_DEFAULT):
        raise Exception('Mock error')  # pylint: disable=broad-exception-raised

    mock_external = job_input.get('mock_external', MOCK_EXTERNAL_DEFAULT)
    if mock_external.get('error_job_return', False):
        rp_http.JOB_DONE_URL = 'https://smartmetal.ai/dev'

    return job_input


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--generator', action='store_true', default=False,
                        help='Starts serverless with the generator_handler')
    parser.add_argument('--async_generator', action='store_true', default=False,
                        help='Starts serverless with the async_generator_handler')
    parser.add_argument('--return_aggregate_stream', action='store_true', default=False,
                        help='Aggregate the stream of generator_handler and return it as a list')

    # Pass the unknown arguments to the serverless
    args, unknown = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + unknown

    # Start the serverless worker
    if args.generator:
        print('Starting serverless with generator_handler')
        print(f"return_aggregate_stream: {args.return_aggregate_stream}")

        runpod.serverless.start({
            "handler": generator_handler,
            "return_aggregate_stream": args.return_aggregate_stream
        })

    elif args.async_generator:
        print('Starting serverless with async_generator_handler')
        print(f"return_aggregate_stream: {args.return_aggregate_stream}")

        runpod.serverless.start({
            "handler": async_generator_handler,
            "return_aggregate_stream": args.return_aggregate_stream,
            "concurrency_modifier": concurrency_modifier
        })

    else:
        runpod.serverless.start({"handler": handler})


##
#

