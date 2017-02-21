from .sdltm2tmx import run


def main():
    src = input('Path to sdltm > ')
    tmx_save_root = input('Directory to save tmx in > ')
    run(src, tmx_save_root)
