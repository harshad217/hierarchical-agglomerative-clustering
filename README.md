<h2>Hierarchical Agglomerative Clustering</h2>

<h3>The program performs Hierarchical Agglomerative Clustering on any dataset that is defined in the following format. Principle Component Analysis is also implemented to better visualize the 'm' dimensional datapoints (and the clusters) in two dimensional space.</h3>

---
<h4>Dataset Format (Columns):</h4>
ID Groundtruth Attribute1 Attribute2 ... Attribute'M'

Each row represent a datapoint.
The first column is the point_id. 
The second column is the groundtruth, specifying which cluster a datapoint actually belongs to. (Required for calculating External Index, Jaccard or RAND)
All the remaining columns represent the attributes of the datapoints. (Each attibute can be considered as a dimension.) 
(All the values should be space separated.)

---