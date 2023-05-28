pip install --upgrade openai
export OPENAI_API_KEY="YOUR API KEY"
openai tools fine_tunes.prepare_data -f prompts.json --suffix "prompts_new.jsonl"
openai api fine_tunes.create -t prompts_new.jsonl -m ada --suffix "pernance"
