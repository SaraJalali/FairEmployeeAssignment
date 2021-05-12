On Measuring the Diversity of Organizational Networks

Published in: CompleNet 2021

Authors: Zeinab S. Jalali, Krishnaram Kenthapadi, and Sucheta Soundarajan1

Abstract: The interaction patterns of employees in social and professional networks play an important role in the success of employees and organizations as a whole. However, in many fields there is a severe under-representation of mi- nority groups; moreover, minority individuals may be segregated from the rest of the network or isolated from one another. While the problem of increasing the representation of minority groups in various fields has been well-studied, diver- sification in terms of numbers alone may not be sufficient: social relationships should also be considered. In this work, we consider the problem of assigning a set of employment candidates to positions in a social network so that diversity and overall fitness are maximized, and propose Fair Employee Assignment (FairEA), a novel algorithm for finding such a matching. The output from FairEA can be used as a benchmark by organizations wishing to evaluate their hiring and assignment practices. On real and synthetic networks, we demonstrate that FairEA does well at finding high-fitness, high-diversity matchings.

Proposed Method: FairEA. (FairEA.py)
FairEmployeeAssignment (FairEA),a method for assigning candidates to positions with the goals of maximizing fitness and diversity.
Input: An undirected professional network G = (P, E), m open positions,  a set of t candidates, fitness of each candidate cj for each open position  oi as wij and an attribute of interest (class)
Output: A matching of candidates to open positions

Baseline Methods:
  1) Random (Random.py)
  2) Weighted Hungarian (Hungarian.py)
  3) Optimization (IPOPT.py)
  
Datasets: (DS/datsets)
  Real Networks : Norwegian Interlocking Directorate (Nor), Consulting Company (CN) and Research Team (RT)
  Synthetic Networks: functional organization (FO), divisional organization (DO), Scale Free -Power Law (SF)

Experiments:
  1) FairEA Evaluation: (Experiments_Evaluation.py)
  2) Example of usage of FairEA:  (Experiments_CaseStudy.py) 
  
