import os, torch, numpy as np
from algorithms.laughs.utils import dataset_utils, audio_utils, data_loaders, torch_utils
from tqdm import tqdm
from functools import partial
from algorithms.laughs.laugh_segmenter import lowpass, get_laughter_instances

from algorithms.laughs.configs import (
    CONFIG_MAP, MODEL_PATH, CONFIG, DEVICE,
    MIN_LENGTH, SAVE_TO_AUDIO_FILES, SAVE_TO_TEXTGRID
)

THRESHOLDS = [0.1 * i for i in range(1,8)]

sample_rate = 8000


def load_model(audio_path: str, config):
    model = config['model'](dropout_rate=0.0, linear_layer_size=config['linear_layer_size'],
                            filter_sizes=config['filter_sizes'])
    feature_fn = config['feature_fn']
    model.set_device(DEVICE)

    if os.path.exists(MODEL_PATH):
        torch_utils.load_checkpoint(MODEL_PATH + '/best.pth.tar', model)
        model.eval()
    else:
        raise Exception(f"Model checkpoint not found at {MODEL_PATH}")
    return model, feature_fn


def load_features(audio_path, config, feature_fn):
    inference_dataset = data_loaders.SwitchBoardLaughterInferenceDataset(
        audio_path=audio_path, feature_fn=feature_fn, sr=sample_rate)

    collate_fn = partial(audio_utils.pad_sequences_with_labels,
                         expand_channel_dim=config['expand_channel_dim'])

    inference_generator = torch.utils.data.DataLoader(
        inference_dataset, num_workers=4, batch_size=8, shuffle=False, collate_fn=collate_fn)
    return inference_generator


def make_predictions(model, inference_generator)-> np.ndarray:
    probabilities = []
    for model_inputs, _ in tqdm(inference_generator):
        x = torch.from_numpy(model_inputs).float().to(DEVICE)
        predictions = model(x).cpu().detach().numpy().squeeze()
        if len(predictions.shape) == 0:
            predictions = [float(predictions)]
        else:
            predictions = list(predictions)
        probabilities += predictions
    probabilities = np.array(probabilities)
    return probabilities


def get_laughing_instances(audio_path: str, probabilities: np.ndarray):
    file_length = audio_utils.get_audio_length(audio_path)
    fps = len(probabilities) / float(file_length)

    probabilities = lowpass(probabilities)
    instances = [get_laughter_instances(probabilities, threshold=threshold, min_length=MIN_LENGTH, fps=fps) for threshold in THRESHOLDS]

    return instances


def draw_laughs_graphic(laugh_instances: list):
    points = []
    for i in range(len(laugh_instances)):
        instances = laugh_instances[i]
        for ins in instances:
            points.append([ins[0], i * 0.1 / 0.7])
            points.append([ins[1], i * 0.1 / 0.7])
    points.sort()
    points = np.array(points)
    return points


def generate_laugh_predictions(audio_path: str):
    config = CONFIG_MAP[CONFIG]
    model, feature_fn = load_model(audio_path, config)
    inference_generator = load_features(audio_path, config, feature_fn)
    probabilities = make_predictions(model, inference_generator)
    laugh_instances = get_laughing_instances(audio_path, probabilities)
    points = draw_laughs_graphic(laugh_instances)
    return points

