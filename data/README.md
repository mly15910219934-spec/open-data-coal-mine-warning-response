# Data provenance and access

## UCI Seismic-bumps

Dataset DOI: https://doi.org/10.24432/C5W902

Official download: https://archive.ics.uci.edu/static/public/266/seismic+bumps.zip

The bundled `raw/seismic-bumps.arff` is the original analysis input (2584 records; 170 positive, 2414 negative; 18 predictors). SHA-256: `aabe512fab65b36d1dfb462650b75cfd8d99d8cc2723e8ecb4e6f5e1caccd5a7`.

The source ZIP is retained beside the ARFF. No missing values are imputed. There are four categorical variables and fourteen numeric variables; categorical one-hot encoding and LR/SVM scaling are fitted within the appropriate training Pipeline. See the frozen configuration. Dataset rights remain those of its source; this package does not grant new rights over third-party data.

## Public case sources

`public_cases/source_package_inventory.csv` lists every member of the separately supplied `Final_Coder_Source_Package.zip`, with case ID, uncompressed size and SHA-256. Subdirectories S1-01 through S1-32 correspond to that inventory.

The approximately 2.4 GB third-party source archive is not duplicated inside the software ZIP pending author confirmation of redistribution scope. Preserve it separately; both coders should use the same frozen files and compare hashes. Source availability is not a finding about any P/W/D/A/V/F element. This release performs no case recoding, does not generate agreement results and cannot substitute for a verified final S1 coding workbook. The archive inventory does not independently certify each report's factual completeness or identity.

The public-record sample is purposive and non-exhaustive, not an industry statistical sample. These case files are not input to Tables 4, 5 or the S4 model bootstrap calculation. All numerical model analyses can run offline with the bundled UCI snapshot.

`public_cases/legacy_baseline/` retains the original baseline coding and screening inputs solely so the historical case-summary code remains usable. These are historical, unchanged records, not the current final consensus S1 Table and not newly verified source judgments. Never substitute them for the independently completed final coding workbook.

## Dataset license and attribution

Sikora, M. & Wrobel, L. (2010). seismic-bumps [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W902 . The unchanged raw dataset is CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), as stated by the official UCI record. MIT does not replace this third-party license.
