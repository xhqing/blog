# Data Hierarchy
Each company's business can be layered according to its own business needs; Currently more popular data layer: **Data Operation Layer**, **Data Warehouse Layer**, **Data Service Layer**.

## Data Operation Layer
**Operation Data Store, ODS**. Data preparation area, also known as **Paste Source Layer**. The main functions of this layer:

- The ODS is the staging area for the back data warehouse layer
- Provide raw data for the DWD layer
- Reduce the impact on business systems
- In order to consider the subsequent need to trace the data, it is not recommended to do too much data cleaning for this layer, just access the original data intact

The data in this layer is the source of processing data in the subsequent data warehouse.

## Data Warehouse Layer
Data warehouse layer can be divided into three layers from top to bottom: **Data Detail Layer**, **Data Intermediate Layer**, **Data Service Layer**.

### Data Detail Layer
**Data Warehouse Details, DWD**.

This layer is the isolation layer between the business layer and the data warehouse, and maintains the same data granularity as the ODS layer. It is mainly for ODS data layer to do some data cleaning and standardized operations, such as removing empty data, dirty data, outliers and so on.

In order to improve the ease of use of the Data Detail Layer, this layer usually adopts some dimension degradation methods to degrade the dimensions to the fact table and reduce the association between the fact table and the dimension table.

### Data Middle Layer
**Data Warehouse Middle, DWM**.

Based on the data of the DWD layer, this layer performs some slight aggregation operations on the data to generate some intermediate result tables, so as to improve the reusability of common indicators and reduce the work of repeated processing. 

In short, aggregate the common core dimensions and calculate the corresponding statistical indicators.

### Data Service Layer
**Data Warehouse Service, DWS**.

This layer is a **Data Service Layer** based on the basic data on DWM, which is integrated and summarized **to analyze a topic domain**. Generally, it is a wide table, which is used to provide follow-up business queries, OLAP analysis, data distribution, etc.

In general, this layer will have relatively few data tables; A table covers a large amount of business content. Because it has many fields, it is also called a wide table.

## Data Application Layer
**Application Data Service, ADS**.

This layer mainly provides data for data products and data analysis, which is generally stored in ES, Redis, PostgreSQL and other systems for online system use. It can also be stored in Hive or Druid for data analysis and data mining. For example, common data reports are stored here.
