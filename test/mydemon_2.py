from camera import Camera
from pathlib import Path

if __name__ == "__main__":
    image_path = Path('../imgs/input')
    for ext in ('*.jpg', '*.jpeg'):
        for image in image_path.glob(ext):
            try:
                camera = Camera(image)
                info = camera.info
                print(info.model)
            except Exception as e:
                print(f'FAIL {image}: {e}')

