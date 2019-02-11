import click
import subprocess
import settings


def log_version(target_dir):
    """
    Creates a logfile that contains information on the currently used generator
    version and saves it in the specified directory.

    Parameters
    ----------
    target_dir : String
        The directory to save the version file in.
    """
    # create version logfile
    version_log = "Git HEAD points at " \
        + subprocess.check_output(['git', 'rev-parse',
                                   'HEAD']).decode('utf-8') \
        + "Git Status says:\n" \
        + subprocess.check_output(['git', 'status']).decode('utf-8')
    with open(target_dir + 'version.log', 'w') as version_logfile:
        version_logfile.write(version_log)


@click.command()
@click.argument('mode')
def main(mode):
    if mode == 'fake_data':
        log_version(settings.FAKE_DATA_DIR)
    elif mode == 'real_data':
        log_version(settings.DATA_DIR)
    elif mode == 'photons':
        log_version(settings.PHOTON_DIR)


if __name__ == "__main__":
    main()
