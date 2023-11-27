# coffee-cluster ☕ 💻
Coffee Blend Clustering using Sentence Transformers & K-Means

---

### Hosted at https://coffee-cluster.streamlit.app/

---

### Data Exploration
| Field        | Description                                           |
|--------------|-------------------------------------------------------|
| `name`       | Name of the blend                                     |
| `roaster`    | Name of the roaster                                   |
| `roast`      | Type of roast (Light, Medium-Light, Medium, Medium-Dark, Dark) |
| `loc_country`| Location of the roaster                               |
| `origin_1`   | Origin of the beans                                   |
| `origin_2`   | Origin of the beans                                   |
| `100g_USD`   | Price per 100g of beans in US dollars                 |
| `rating`     | Rating of the coffee                                  |
| `review_date`| Date of the coffee review                             |
| `desc_1`     | Detailed review                                       |
| `desc_2`     | More context about the farms/roasters                 |
| `desc_3`     | Concise review                                        |

### Data Preprocessing
Because our raw dataset contains both structured data and textual descriptions, we preprocess it before running a clustering algorithm.

We one-hot encode the following structured data columns: `origin_1`, `origin_2`. We deliberately leave out the 
`Name`, `roaster`, and `roast` columns, because we want to discover the true similarities between coffee beans from *different* roasters. 

For numerical features, `100g_USD` and `rating`, we use the standard scaler to standardize features by removing the mean and scaling to unit variance.

Of the 3 review columns, `desc_1` and `desc_3` are the most relevant because they contain descriptions of the taste of the coffee itself. Therefore, we only keep these as input data.
In order to vectorize the texts, we use [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) to produce meaningful sentence embeddings:

> Text is embedded in vector space such that similar text are closer and can efficiently be found using cosine similarity.

This is particularly suitable for our task.

### Clustering
After applying PCA for dimensionality reduction, we did clustering using the standard KMeans algorithm with the following hyperparameters:
`n_clusters=20`, 
`n_init=’auto’`,
`max_iter=1000`,
`random_state=42`.

### Results
<img width="617" alt="Screenshot 2023-11-27 at 02 20 54" src="https://github.com/ronyw7/coffee-cluster/assets/78146401/64cf1c35-49d5-409d-ae89-f5d0e23a2c63">
<img width="617" alt="Screenshot 2023-11-27 at 02 20 54" src="https://github.com/ronyw7/coffee-cluster/assets/78146401/9bb86f7c-ab3e-45d1-a195-fb1b179d504f">




### Examples
Cluster 7: sweet, smoky, dark-roasted
Example Reviews:
> Brisk, dry, sweetly vegetal. Green bean, carob, charred balsa, faded gardenia, raw almond in aroma and cup. Flatly bittersweet structure with inert acidity; dry, rather thin mouthfeel. Wood-framed, sweetly vegetal finish. (Pike’s Place Blend, Starbucks Coffee)

> Cocoa-toned, gently roasty. Cocoa powder, lightly scorched cedar, Brazil nut, raisin, lily in aroma and cup. Sweet-savory structure with barely perceptible acidity; velvety, heavyish mouthfeel. Gently drying wood-framed finish with hints of cocoa powder and lily. (Amazon Haze, 421 Brew House)

> Roast-prominent, chocolaty, wood-framed. Dark chocolate, lily-like flowers, raisin, scorched fir, brown sugar in aroma and cup. Sweet-savory structure with mild acidity; full, satiny mouthfeel. The gently drying, chocolaty finish is supported by smoky fir and raisin notes. (Peaberry Blend, San Francisco Bay Coffee)



