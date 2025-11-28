import pandas as pd

# Read results
results = pd.read_csv('bird_detection/results.csv')

# Get final epoch (last row)
final = results.iloc[-1]

print("📊 Final Training Metrics:")
print(f"Final Loss: {final['train/box_loss']:.3f}")
print(f"mAP@50: {final['metrics/mAP50(B)']:.3f}")
print(f"mAP@50-95: {final['metrics/mAP50-95(B)']:.3f}")
print(f"Precision: {final['metrics/precision(B)']:.3f}")
print(f"Recall: {final['metrics/recall(B)']:.3f}")

# For README table
print("\n📋 Copy this for README:")
print(f"| Final Loss | {final['train/box_loss']:.3f} |")
print(f"| mAP@50 | {final['metrics/mAP50(B)']:.3f} |")
print(f"| mAP@50-95 | {final['metrics/mAP50-95(B)']:.3f} |")
print(f"| Precision | {final['metrics/precision(B)']:.3f} |")
print(f"| Recall | {final['metrics/recall(B)']:.3f} |")

