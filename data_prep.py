import pandas as pd
import numpy as np

# Use 'Dataset' to match actual folder name
df = pd.read_csv('Dataset/marketing_campaign_dataset.csv')
df['brand'] = df['Company']
df['audience_size_mailed'] = np.random.randint(10000, 500000, len(df))
df['total_cost'] = df['audience_size_mailed'] * 0.65
df['response_rate'] = df['Conversion_Rate'] * 0.8
df['responses'] = df['audience_size_mailed'] * df['response_rate']
df['revenue'] = df['total_cost'] * (1 + df['ROI'])
df['cpa'] = df['total_cost'] / df['responses']
df['roas'] = df['revenue'] / df['total_cost']

enriched = df[['Campaign_ID', 'brand', 'Campaign_Type', 'Target_Audience',
'Duration', 'Channel_Used', 'Location', 'Conversion_Rate',
'Acquisition_Cost', 'ROI', 'audience_size_mailed', 'total_cost',
'responses', 'revenue', 'cpa', 'roas', 'response_rate']]

# Save to Dataset folder
enriched.to_csv('Dataset/direct_mail_campaigns_enriched.csv', index=False)
print(enriched.head())
