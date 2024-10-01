import numpy as np

def compute_metrics(pred, task_config='multi-label-classification'):
    logits, labels = pred
    if task_config == 'multi-class-classification':
        preds = np.argmax(logits, axis=1) 
        accuracy = np.mean(preds == labels)
        return {"accuracy": accuracy}
    elif task_config == 'multi-label-classification':
        res = {}
        for k in range(3, 4):
            temp_logits = np.zeros_like(logits)
            for i, output in enumerate(logits):
                topk_indices = np.argsort(output)[-k:]
                mask = np.zeros_like(output)
                mask[topk_indices] = 1
                temp_logits[i,:] = mask

            matches = temp_logits * labels
            
            # Single-match Accuracy
            correct_predictions = (matches.sum(axis=1) > 0).sum()
            total_samples = len(labels)
            one_match_accuracy = correct_predictions / total_samples

            # Recall
            correct_predictions = (matches.sum(axis=1)).sum()
            total_samples = (labels.sum(axis=1)).sum()
            recall = correct_predictions / total_samples

            one_match_accuracy_label = f'one_match_accuracy_k={k}'
            recall_label = f'recall@{k}'
            res[one_match_accuracy_label] = one_match_accuracy
            res[recall_label] = recall
        
        return res