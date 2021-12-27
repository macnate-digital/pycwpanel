import click
import os
import time
import tomli_w

"""
This script helps in setting up CWP settings which the
pwcwpanel will use.

The required settings variables include:

- AWS_S3_BUCKET
- AWS_S3_KEY
- AWS_S3_ACCESS_KEY_ID
- AWS_S3_SECRET_ACCESS_KEY
- CWP_API_URL
- CWP_API_KEY
"""


def cwp_setup_prompts() -> None:

    WELCOME_BANNER = """
    ===========================================================
        👋👋 Hi there! Thank you for choosing pycwpanel!
    ===========================================================

    This utility will help you set up a few things that pycwpanel
    requires to function properly.

    Follow the prompts and you're {set,}!
    """

    # Welcome banner
    click.echo(message=WELCOME_BANNER)

    # def cwp_setup_prompts():

    time.sleep(3)
    AWS_S3_BUCKET = click.prompt(
        "Enter AWS S3 bucket name")

    AWS_S3_KEY = click.prompt(
        "Enter AWS S3 key/subdirectory")

    AWS_S3_ACCESS_KEY_ID = click.prompt(
        "Enter AWS S3 Access Key ID")

    AWS_S3_SECRET_ACCESS_KEY = click.prompt(
        "Enter AWS S3 Secret Access Key: ")

    CWP_API_URL = click.prompt(
        "Enter CWP API URL - Leave empty for default",
        default="https://localhost:2304")

    CWP_API_KEY = click.prompt(
        "Enter CWP API KEY (from API Manager under CWP Settings)")

    CWP_API_HOSTNAME = click.prompt(
        "Enter CWP server hostname e.g. cwp.myhostingcompany.com)",)

    toml_data = {
        "AWS_S3_BUCKET": AWS_S3_BUCKET,
        "AWS_S3_KEY": AWS_S3_KEY,
        "AWS_ACCESS_KEY_ID": AWS_S3_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_S3_SECRET_ACCESS_KEY,
        "CWP_API_URL": CWP_API_URL,
        "CWP_API_KEY": CWP_API_KEY,
        "CWP_API_HOSTNAME": CWP_API_HOSTNAME
    }

    # Write the above to a toml file
    try:
        with open("cwp_settings.toml", "wb") as f:

            tomli_w.dump(toml_data, f)

            click.secho(
                "\n✅ Settings successfully written to cwp_settings.toml",
                fg="green")
    except Exception as e:
        click.secho(
            f"""
            ❌ Failed to write settings to cwp_settings.toml.
            See more info on the error below\n{e}""", fg="red"
        )


def cwp_setup() -> None:

    # Check if file exists and ask for overwrite confirmation
    try:
        if os.path.exists("cwp_settings.toml"):
            click.secho(
                """\n⚠ ATTENTION! ⚠""",
                fg='bright_yellow',
                blink=True)

            click.confirm(
                click.style(
                    "A CWP settings file was found. Are"
                    " you sure you want to overwrite it?"))

        # Prompt the user normally if settings file is not found
        cwp_setup_prompts()

    except click.Abort:
        click.echo(
            "Aborting... Goodbye!"
        )
