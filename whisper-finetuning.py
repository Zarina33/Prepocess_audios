import torch
from datasets import Dataset, Audio
from transformers import WhisperProcessor, WhisperForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer
import os
from pathlib import Path
import pandas as pd
from typing import Dict, List, Union

def prepare_dataset(
    audio_dir: str,
    transcription_file: str = None,
    sampling_rate: int = 16000
) -> Dataset:
    """
    Prepare the dataset for training.
    
    Args:
        audio_dir: Directory containing WAV files
        transcription_file: Optional path to transcription file
        sampling_rate: Target sampling rate for audio
    """
    # Get all wav files
    audio_files = list(Path(audio_dir).glob("**/*.wav"))
    
    # If transcription file exists, load it
    if transcription_file and os.path.exists(transcription_file):
        transcriptions = pd.read_csv(transcription_file)
        # Assuming format: filename,transcription
        trans_dict = dict(zip(transcriptions['filename'], transcriptions['transcription']))
    else:
        # If no transcriptions provided, create empty ones
        trans_dict = {f.name: "" for f in audio_files}
    
    # Create dataset dictionary
    dataset_dict = {
        "audio": [str(f) for f in audio_files],
        "transcription": [trans_dict.get(f.name, "") for f in audio_files]
    }
    
    # Create Dataset object
    dataset = Dataset.from_dict(dataset_dict)
    
    # Add audio loading
    dataset = dataset.cast_column("audio", Audio(sampling_rate=sampling_rate))
    
    return dataset

def preprocess_function(
    examples: Dict[str, Union[str, List]],
    processor: WhisperProcessor
) -> Dict[str, torch.Tensor]:
    """
    Preprocess the dataset examples.
    """
    # Load and resample audio
    audio = [x["array"] for x in examples["audio"]]
    
    # Compute input features
    inputs = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )
    
    # Compute labels
    labels = processor(
        text=examples["transcription"],
        return_tensors="pt",
        padding=True
    ).input_ids
    
    return {
        "input_features": inputs.input_features,
        "labels": labels
    }

def main():
    # Initialize model and processor
    model_name = "openai/whisper-tiny"
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    
    # Set the language and task
    processor.tokenizer.set_prefix_tokens(language="ky", task="transcribe")
    
    # Prepare dataset
    dataset = prepare_dataset(
        audio_dir="path/to/your/wav/files",
        transcription_file="path/to/your/transcriptions.csv"
    )
    
    # Split dataset
    dataset_split = dataset.train_test_split(test_size=0.1)
    
    # Preprocess dataset
    processed_dataset = dataset_split.map(
        lambda x: preprocess_function(x, processor),
        remove_columns=dataset_split["train"].column_names,
        batch_size=8,
        batched=True
    )
    
    # Define training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-ky-tiny",
        per_device_train_batch_size=16,
        gradient_accumulation_steps=2,
        learning_rate=1e-5,
        warmup_steps=500,
        max_steps=4000,
        gradient_checkpointing=True,
        fp16=True,
        evaluation_strategy="steps",
        eval_steps=1000,
        save_steps=1000,
        logging_steps=25,
        report_to=["tensorboard"],
        load_best_model_at_end=True,
        greater_is_better=False,
        metric_for_best_model="wer",
        push_to_hub=False,
    )
    
    # Initialize trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=processed_dataset["train"],
        eval_dataset=processed_dataset["test"],
    )
    
    # Start training
    trainer.train()
    
    # Save the model
    trainer.save_model("./whisper-ky-tiny-final")

if __name__ == "__main__":
    main()
