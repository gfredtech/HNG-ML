from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import skimage

from sklearn import svm, metrics, datasets
from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split

from skimage.io import imread
from skimage.transform import resize


def load_image_files(container_path, dimension=(64, 64, 3)):
    """
    Load image files with categories as subfolder names
    which performs like scikit-learn sample dataset

    Parameters
    ----------
    container_path : string or unicode
        Path to the main folder holding one subfolder per category
    dimension : tuple
        size to which image are adjusted to

    Returns
    -------
    Bunch
    """
    image_dir = Path(container_path)
    folders = [directory for directory in image_dir.iterdir() if directory.is_dir()]
    categories = [fo.name for fo in folders]
    print("Categories:", categories)

    descr = "A image classification dataset"
    images = []
    flat_data = []
    target = []
    for i, direc in enumerate(folders):
        for file in direc.iterdir():
            img = skimage.io.imread(file)
            img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
            flat_data.append(img_resized.flatten())
            images.append(img_resized)
            target.append(i)
    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)

    return Bunch(data=flat_data,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=descr)


if __name__ == '__main__':
    image_dataset = load_image_files("HNG/")
    print("Stage 2")
    X_train, X_test, y_train, y_test = train_test_split(
        image_dataset.data, image_dataset.target, test_size=0.3, random_state=109)
    print("Stage 3")
    param_grid = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
    ]
    print("Stage 4")
    svc = svm.SVC()
    print("Stage 5")
    clf = GridSearchCV(svc, param_grid)
    print("Stage 6")
    clf.fit(X_train, y_train)
    print("Stage 7")
    y_pred = clf.predict(X_test)
    print("Stage 8")
    print("Classification report for - \n{}:\n{}\n".format(
        clf, metrics.classification_report(y_test, y_pred)))
