# %%
import pandas as pd

# Load monitoring from csv
monitoring = pd.read_csv('monitoring.csv', header=None)

# Add columns
monitoring.columns = ['timestamp', 'model', 'solution', 'prompt_tokens', 'completion_tokens']
prompt_pricing={'gpt-35-turbo':0.0000014, 'gpt-4':0.000028}
completion_pricing={'gpt-35-turbo':0.0000019, 'gpt-4':0.000056}
# Add cost column for each row
monitoring['prompt_cost'] = monitoring['prompt_tokens'] * monitoring['model'].map(prompt_pricing)
monitoring['completion_cost'] = monitoring['completion_tokens'] * monitoring['model'].map(completion_pricing)
monitoring['total_cost'] = monitoring['prompt_cost'] + monitoring['completion_cost']

#Display
# Print in green the monitoring table
print("\033[92m###   Costs Table   ### \033[0m")
print(monitoring)


# %%
# Cost per solution
print("")
print("")
print("\033[92m###   Total cost per solution   ###\033[0m")
print(monitoring.groupby('solution').sum()[['prompt_cost', 'completion_cost', 'total_cost']])


