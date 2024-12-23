import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.metrics.distance import edit_distance
import sacrebleu

smoothie = SmoothingFunction().method1

def compute_exact_match(reference, prediction):
    return int(reference.strip() == prediction.strip())

def compute_bleu(reference, prediction):
    reference_tokens = reference.split()
    prediction_tokens = prediction.split()
    
    if not reference_tokens or not prediction_tokens:
        return 0
    
    return sentence_bleu([reference_tokens], prediction_tokens, smoothing_function=smoothie)

def compute_chrf(reference, prediction):
    chrf_scorer = sacrebleu.CHRF()
    
    if not reference or not prediction:
        return 0.0
    
    return chrf_scorer.sentence_score(prediction, [reference]).score

def compute_edit_distance(reference, prediction):
    return edit_distance(reference, prediction)

def compute_metrics(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    exact_matches = []
    bleu_scores = []
    chrf_scores = []
    edit_distances = []

    for _, row in df.iterrows():
        reference = row['code examples']
        prediction = row['completion']
        
        exact_matches.append(compute_exact_match(reference, prediction))
        bleu_scores.append(compute_bleu(reference, prediction))
        chrf_scores.append(compute_chrf(reference, prediction))
        edit_distances.append(compute_edit_distance(reference, prediction))
    
    df['exact_match'] = exact_matches
    df['bleu'] = bleu_scores
    df['chrf'] = chrf_scores
    df['levenshtein_distance'] = edit_distances
    
    df.to_csv(output_csv, index=False)

    return df


