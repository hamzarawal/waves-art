import numpy as np
import cv2
import tqdm
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", help="path to the image", required=True)
    parser.add_argument("--patch_size", default="15", help="patch size")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    img = cv2.imread(args.image_path, 0)

    patch_size = int(args.patch_size)
    img_waves = np.ones(img.shape) * 255

    # loop through the image to pick patches
    for i in tqdm.tqdm(range(0, img.shape[0]-patch_size, patch_size)):
        for j in range(0, img.shape[1]-patch_size, patch_size):
            patch = img[i:i+patch_size, j:j+patch_size]

            # find blackness_score of the patch. This will be used to adjust freq and amp of the sine wave
            blackness_score = np.sum(patch) / patch_size**2

            # calculate the frequency and amplitude of the sine wave
            e = 0.0000000001
            freq = (2*np.pi)/patch_size * np.log(np.sqrt(blackness_score)+e)
            amp = (1*patch_size) * (1-blackness_score/ 255)

            # create the sine wave
            x = np.arange(0, patch_size, 1)
            y = amp * np.sin(freq * x) - patch_size

            # ajdust the range to correspond to coordinates of the image
            x += j
            y = np.int32(np.abs(y/2)) + i

            for k in range(x.shape[0]-1):
                cv2.line(img_waves, (x[k], y[k]), (x[k+1], y[k+1]), 0, 1)

    # save the image
    ext = '.'+args.image_path.split(".")[-1]
    img_name = os.path.basename(args.image_path)
    save_path = os.path.join(os.path.dirname(args.image_path), img_name.replace(ext,"_waves.png"))
    cv2.imwrite(save_path, img_waves)