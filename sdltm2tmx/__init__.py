# import os

# from .sdltm2tmx import run


# def main():
#     src = input('Path to sdltm > ')
#     src = src.strip('"').strip("'")
#
#     if not os.path.exists(src):
#         raise FileNotFoundError(src)
#
#     if not os.path.isfile(src):
#         raise IsADirectoryError(src)
#
#     if os.path.splitext(src)[1].lower() != '.sdltm':
#         print('Error {} does not look like a valid file'.format(src))
#         return None
#
#     tmx_save_root = input('Directory to save tmx in > ')
#     tmx_save_root = tmx_save_root.strip("'").strip('"')
#     tmx_save_root = os.path.abspath(os.path.expanduser(tmx_save_root))
#
#     if not os.path.exists(tmx_save_root):
#         raise FileNotFoundError(tmx_save_root)
#
#     if not os.path.isdir(tmx_save_root):
#         raise NotADirectoryError
#
#     run(src, tmx_save_root)
