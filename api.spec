#Last modified: 2020-04-30
openapi: 3.0.0
info:
  description: >-
    The FoodData Central API provides REST access to FoodData Central (FDC). It is intended primarily to assist application developers wishing to incorporate nutrient data into their applications or websites.
      To take full advantage of the API, developers should familiarize themselves with the database by reading the database documentation available via links on [Data Type Documentation](https://fdc.nal.usda.gov/data-documentation.html). This documentation provides the detailed definitions and descriptions needed to understand the data elements referenced in the API documentation.
      
      Additional details about the API including rate limits, access, and licensing are available on the [FDC website](https://fdc.nal.usda.gov/api-guide.html)
  version: 1.0.1
  title: Food Data Central API
  contact:
    name: Food Data Central Contact Form
    url: https://nal.altarama.com/reft100.aspx?key=FoodData
  license:
    name: Creative Commons 0 1.0 Universal
    url: 'https://creativecommons.org'
servers:
  - url: https://api.nal.usda.gov/fdc
security:
  - ApiKeyAuth: []
tags:
- name: FDC
  description: endpoints to retrieve nutrient data
        
paths:
  '/v1/food/{fdcId}':
    get:
      tags: 
        - FDC
      security:
        - ApiKeyAuth: []
      summary: Fetches details for one food item by FDC ID
      description:  Retrieves a single food item by an FDC ID. Optional format and nutrients can be specified.
      operationId: getFood
      parameters:
        - in: path
          name: fdcId
          description: FDC id of the food to retrieve
          required: true
          schema:
           type: string
        - in: query
          name: format
          description: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
          required: false
          schema:
            type: string
            enum: [abridged, full]
        - in: query
          name: nutrients
          description: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
          schema:
            type: array
            minItems: 1
            maxItems: 25
            items:
              type: integer
            example: [203, 204, 205]
      responses:
        '200':
          description: One food result.
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/AbridgedFoodItem'
                  - $ref: '#/components/schemas/BrandedFoodItem'
                  - $ref: '#/components/schemas/FoundationFoodItem'
                  - $ref: '#/components/schemas/SRLegacyFoodItem'
                  - $ref: '#/components/schemas/SurveyFoodItem'
        '400':
          description: bad input parameter
        '404':
          description: no results found
          
  '/v1/foods':
    get:
      tags: 
      - FDC
      summary: Fetches details for multiple food items using input FDC IDs
      description:  Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified. Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
      operationId: getFoods
      parameters:
        - in: query
          name: fdcIds
          required: true
          description: List of multiple FDC ID's. Should be comma separated list (e.g. fdcIds=534358,373052) or repeating parameters (e.g. fdcIds=534358&fdcIds=373052).
          schema:
            type: array
            minItems: 1
            maxItems: 20
            items:
              type: string
            example: [534358,373052,616350]
        - in: query
          name: format
          description: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
          required: false
          schema:
            type: string
            enum: [abridged, full]
        - in: query
          name: nutrients
          description: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
          schema:
            type: array
            minItems: 1
            maxItems: 25
            items:
              type: integer
            example: [203, 204, 205]
      responses:
        '200':
          description: List of Food details matching specified FDC ID's. Invalid FDC ID's or ones that are not found are omitted.
          content:
            application/json:
             schema:
              type: array
              items:
                anyOf:
                  - $ref: '#/components/schemas/AbridgedFoodItem'
                  - $ref: '#/components/schemas/BrandedFoodItem'
                  - $ref: '#/components/schemas/FoundationFoodItem'
                  - $ref: '#/components/schemas/SRLegacyFoodItem'
                  - $ref: '#/components/schemas/SurveyFoodItem'
        '400':
          description: bad input parameter
          
    post:
      tags: 
      - FDC
      summary: Fetches details for multiple food items using input FDC IDs
      description:  Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified. Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
      operationId: postFoods
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FoodsCriteria'
      responses:
        '200':
          description: List of Food details matching specified FDC ID's. Invalid FDC ID's or ones that are not found are omitted.
          content:
            application/json:
             schema:
              type: array
              items:
                anyOf:
                  - $ref: '#/components/schemas/AbridgedFoodItem'
                  - $ref: '#/components/schemas/BrandedFoodItem'
                  - $ref: '#/components/schemas/FoundationFoodItem'
                  - $ref: '#/components/schemas/SRLegacyFoodItem'
                  - $ref: '#/components/schemas/SurveyFoodItem'
        '400':
          description: bad input parameter
          
          
  '/v1/foods/list':
    get:
      tags: 
      - FDC
      summary: Returns a paged list of foods, in the 'abridged' format
      description:  Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.
      operationId: getFoodsList
      parameters:
        - in: query
          name: dataType
          description: Optional. Filter on a specific data type; specify one or more values in an array.
          schema:
            type: array
            items:
              type: string
              enum:
                - Branded
                - Foundation
                - Survey (FNDDS)
                - SR Legacy
            minItems: 1
            maxItems: 4
          explode: false
          style: form
          example: ["Foundation","SR Legacy"]
        - in: query
          name: pageSize
          description: Optional. Maximum number of results to return for the current page. Default is 50.
          schema:
            type: integer
            minimum: 1
            maximum: 200
          example: 25
        - in: query
          name: pageNumber
          description: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
          schema:
            type: integer
            example: 2
        - in: query
          name: sortBy
          description: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases. 
          schema:
            type: string
            enum:
              - dataType.keyword
              - lowercaseDescription.keyword
              - fdcId
              - publishedDate
        - in: query
          name: sortOrder
          description: Optional. The sort direction for the results. Only applicable if sortBy is specified.
          schema:
            type: string
            enum:
              - asc
              - desc
      responses:
        '200':
          description: List of foods for the requested page
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AbridgedFoodItem'
        '400':
          description: bad input parameter
          
    post:
      tags: 
      - FDC
      summary: Returns a paged list of foods, in the 'abridged' format
      description:  Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.
      operationId: postFoodsList
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FoodListCriteria'
      responses:
        '200':
          description: List of foods for the requested page
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AbridgedFoodItem'
        '400':
          description: bad input parameter
                
  '/v1/foods/search':
    get:
      tags: 
      - FDC
      summary: Returns a list of foods that matched search (query) keywords
      description: Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes or sorting. 
      operationId: getFoodsSearch
      parameters:
        - in: query
          name: query
          description: One or more search terms.  The string may include [search operators](https://fdc.nal.usda.gov/help.html#bkmk-2)
          required: true
          schema:
            type: string
          example: "cheddar cheese"
        - in: query
          name: dataType
          description: Optional. Filter on a specific data type; specify one or more values in an array.
          schema:
            type: array
            items:
              type: string
              enum:
                - Branded
                - Foundation
                - Survey (FNDDS)
                - SR Legacy
            minItems: 1
            maxItems: 4
          explode: false
          style: form
          example: ["Foundation","SR Legacy"]
        - in: query
          name: pageSize
          description: Optional. Maximum number of results to return for the current page. Default is 50.
          schema:
            type: integer
            minimum: 1
            maximum: 200
          example: 25
        - in: query
          name: pageNumber
          description: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
          schema:
            type: integer
            example: 2
        - in: query
          name: sortBy
          description: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases.
          schema:
            type: string
            enum:
              - dataType.keyword
              - lowercaseDescription.keyword
              - fdcId
              - publishedDate
          example: dataType.keyword
        - in: query
          name: sortOrder
          description: Optional. The sort direction for the results. Only applicable if sortBy is specified.
          schema:
            type: string
            enum:
              - asc
              - desc
          example: asc
        - in: query
          name: brandOwner
          description: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
          schema:
            type: string
          example: "Kar Nut Products Company"
      responses:
          '200':
            description: List of foods that matched search terms
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/SearchResult'
          '400':
            description: bad input parameter

    post:
      tags: 
      - FDC
      summary: Returns a list of foods that matched search (query) keywords
      description: Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes or sorting.
      operationId: postFoodsSearch
      requestBody:
        required: true
        description: The query string may also include standard [search operators](https://fdc.nal.usda.gov/help.html#bkmk-2) 
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FoodSearchCriteria'
      responses:
        '200':
          description:  List of foods that matched search terms
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResult'
        '400':
            description: bad input parameter

  '/v1/json-spec':
    get:
      tags: 
      - FDC
      summary: Returns this documentation in JSON format
      description: The OpenAPI 3.0 specification for the FDC API rendered as JSON (JavaScript Object Notation) 
      operationId: getJsonSpec  
      responses:
        'default': 
          description: JSON rendering of OpenAPI 3.0 specification
          
  '/v1/yaml-spec':
    get:
      tags: 
      - FDC
      summary: Returns this documentation in JSON format
      description: The OpenAPI 3.0 specification for the FDC API rendered as YAML (YAML Ain't Markup Language) 
      operationId: getYamlSpec  
      responses:
        'default': 
          description: YAML rendering of OpenAPI 3.0 specification

components:

  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: query
      name: api_key
      
  schemas:
  
    AbridgedFoodItem:
      type: object
      required:
        - fdcId
        - dataType
        - description
      properties:
        dataType:
          type: string
          example: "Branded"
        description:
          type: string
          example: "NUT 'N BERRY MIX"
        fdcId:
          type: integer
          example: 534358
        foodNutrients:
          type: array
          items:
            $ref: '#/components/schemas/AbridgedFoodNutrient'
        publicationDate:
          type: string
          example: "4/1/2019"
        brandOwner:
          type: string
          description: only applies to Branded Foods
          example: "Kar Nut Products Company"
        gtinUpc:
          type: string
          description: only applies to Branded Foods
          example: "077034085228"
        ndbNumber:
          type: integer
          description: only applies to Foundation and SRLegacy Foods
          example: 7954
        foodCode:
          type: string
          description: only applies to Survey Foods
          example: "27415110"
          
    BrandedFoodItem:
      type: object
      required:
        - fdcId
        - dataType
        - description
      properties:
        fdcId:
          type: integer
          example: 534358
        availableDate:
          type: string
          example: "8/18/2018"
        brandOwner:
          type: string
          example: "Kar Nut Products Company"
        dataSource:
          type: string
          example: "LI"
        dataType:
          type: string
          example: "Branded"
        description:
          type: string
          example: "NUT 'N BERRY MIX"
        foodClass:
          type: string
          example: 'Branded'
        gtinUpc:
          type: string
          example: "077034085228"
        householdServingFullText:
          type: string
          example: "1 ONZ"
        ingredients:
          type: string
          example: "PEANUTS (PEANUTS, PEANUT AND/OR SUNFLOWER OIL). RAISINS. DRIED CRANBERRIES (CRANBERRIES, SUGAR, SUNFLOWER OIL). SUNFLOWER KERNELS AND ALMONDS (SUNFLOWER KERNELS AND ALMONDS, PEANUT AND/OR SUNFLOWER OIL)."
        modifiedDate:
          type: string
          example: "8/18/2018"
        publicationDate:
          type: string
          example: "4/1/2019"
        servingSize:
          type: integer
          format: float32
          example: 28
        servingSizeUnit:
          type: string
          example: "g"
        preparationStateCode:
          type: string
          example: "UNPREPARED"
        brandedFoodCategory:
          type: string
          example: "Popcorn, Peanuts, Seeds & Related Snacks"
        tradeChannel:
          type: array
          items:
            type: string
          example: ["CHILD_NUTRITION_FOOD_PROGRAMS", "GROCERY"]
        gpcClassCode:
          type: integer
          example: 50161800
        foodNutrients:
          type: array
          items:
            $ref: '#/components/schemas/FoodNutrient'
        foodUpdateLog:
          type: array
          items:  
            $ref: '#/components/schemas/FoodUpdateLog'
        labelNutrients:
          type: object
          properties:
            fat:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 8.9992
            saturatedFat:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 0.9996
            transFat:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 0
            cholesterol:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 0
            sodium:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 0
            carbohydrates:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 12.0008
            fiber:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 1.988
            sugars:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 7.9996
            protein:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 4.0012
            calcium:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 19.88
            iron:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 0.7196
            potassium:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 159.88
            calories:
              type: object
              properties:
                value:
                  type: number
                  format: float
                  example: 140
              
    FoundationFoodItem:
      required:
        - fdcId
        - dataType
        - description
      properties:
        fdcId:
          type: integer
          example: 747448
        dataType:
          type: string
          example: "Foundation"
        description:
          type: string
          example: "Strawberries, raw"
        foodClass:
          type: string
          example: "FinalFood"
        footNote:
          type: string
          example: "Source number reflects the actual number of samples analyzed for a nutrient. Repeat nutrient analyses may have been done on the same sample with the values shown."
        isHistoricalReference:
          type: boolean
          example: false
        ndbNumber:
          type: integer
          example: 9316
        publicationDate:
          type: string
          example: "12/16/2019"
        scientificName: 
          type: string
          example: "Fragaria X ananassa"
        foodCategory:
          $ref: '#/components/schemas/FoodCategory'
        foodComponents:
          type: array
          items:
            $ref: '#/components/schemas/FoodComponent'
        foodNutrients:
          type: array
          items:
            $ref: '#/components/schemas/FoodNutrient'
        foodPortions:
          type: array
          items:
            $ref: '#/components/schemas/FoodPortion'
        inputFoods:
          type: array
          items:
            $ref: '#/components/schemas/InputFoodFoundation'
        nutrientConversionFactors:
          type: array
          items:
            $ref: '#/components/schemas/NutrientConversionFactors'
            
    SRLegacyFoodItem:
      required:
        - fdcId
        - dataType
        - description
      properties:
        fdcId:
          type: integer
          example: 170379
        dataType:
          type: string
          example: "SR Legacy"
        description:
          type: string
          example: "Broccoli, raw"
        foodClass:
          type: string
          example: "FinalFood"
        isHistoricalReference:
          type: boolean
          example: true
        ndbNumber:
          type: integer
          example: 11090
        publicationDate:
          type: string
          example: "4/1/2019"
        scientificName: 
          type: string
          example: "Brassica oleracea var. italica"
        foodCategory:
          $ref: '#/components/schemas/FoodCategory'
        foodNutrients:
          type: array
          items:
            $ref: '#/components/schemas/FoodNutrient'
        nutrientConversionFactors:
          type: array
          items:
            $ref: '#/components/schemas/NutrientConversionFactors'
            
    SurveyFoodItem:
      required:
        - fdcId
        - dataType
        - description
      properties:
        fdcId:
          type: integer
          example: 337985
        datatype:
          type: string
          example: "Survey (FNDDS)"
        description:
          type: string
          example: "Beef curry"
        endDate:
          type: string
          example: "12/31/2014"
        foodClass:
          type: string
          example: "Survey"
        foodCode:
          type: string
          example: "27116100"
        publicationDate:
          type: string
          example: "4/1/2019"
        startDate:
          type: string
          example: "1/1/2013"
        foodAttributes:
          type: array
          items:
            $ref: '#/components/schemas/FoodAttribute'  
        foodPortions:
          type: array
          items:
            $ref: '#/components/schemas/FoodPortion'
        inputFoods:
          type: array
          items:
            $ref: '#/components/schemas/InputFoodSurvey'
        wweiaFoodCategory:
          $ref: '#/components/schemas/WweiaFoodCategory'
    
    SampleFoodItem:
      required:
        - fdcId
        - dataType
        - description
      properties:
        fdcId:
          type: integer
          example: 45551
        datatype:
          type: string
          example: "Sample"
        description:
          type: string
          example: "Beef, Tenderloin Roast, select, roasted, comp5, lean (34BLTR)"
        foodClass:
          type: string
          example: "Composite"
        publicationDate:
          type: string
          example: "4/1/2019"
        foodAttributes:
          type: array
          items:
            $ref: '#/components/schemas/FoodCategory'  
          
    AbridgedFoodNutrient:
      required:
        - id
        - nutrientNumber
        - unit
      properties:
        number:
          type: integer
          format: uint
          example: 303
        name:
          type: string
          example: "Iron, Fe"
        amount:
          type: number
          format: float
          example: 0.53
        unitName:
          type: string
          example: "mg"
        derivationCode:
          type: string
          example: "LCCD"
        derivationDescription:
          type: string
          example: "Calculated from a daily value percentage per serving size measure"
          
    FoodNutrient:
      required:
        - id
        - nutrientNumber
        - unit
      properties:
        id:
          type: integer
          format: uint
          example: 167514
        amount:
          type: number
          format: float
          example: 0E-8
        dataPoints:
          type: integer
          format: int32
          example: 49
        min:
          type: number
          format: float
          example: 73.73000000
        max:
          type: number
          format: float
          example: 91.80000000
        median:
          type: number
          format: float
          example: 90.30000000
        type:
          type: string
          example: "FoodNutrient"
        nutrient:
          $ref: '#/components/schemas/Nutrient'
        foodNutrientDerivation:
          $ref: '#/components/schemas/FoodNutrientDerivation'
        nutrientAnalysisDetails:
          $ref: '#/components/schemas/NutrientAnalysisDetails'
          
    Nutrient:
      description: a food nutrient
      properties:
        id:
          type: integer
          format: uint
          example: 1005
        number:
          type: string
          example: "305"
        name:
          type: string
          example: "Carbohydrate, by difference"
        rank:
          type: integer
          format: uint
          example: 1110
        unitName:
          type: string
          example: "g"
          
    FoodNutrientDerivation:
      properties:
        id:
          type: integer
          format: int32
          example: 75
        code:
          type: string
          example: "LCCD"
        description:
          type: string
          example: "Calculated from a daily value percentage per serving size measure"
        foodNutrientSource:
          $ref: '#/components/schemas/FoodNutrientSource'
          
    FoodNutrientSource:
      properties:
        id:
          type: integer
          format: int32
          example: 9
        code: 
          type: string
          example: "12"
        description:
          type: string
          example: "Manufacturer's analytical; partial documentation"
          
    NutrientAnalysisDetails:
      properties:
        subSampleId:
          type: integer
          example: 343866
        amount:
          type: number
          format: float
          example: 0E-8
        nutrientId:
          type: integer
          example: 1005
        labMethodDescription:
          type: string
          example: "10.2135/cropsci2017.04.0244"
        labMethodOriginalDescription:
          type: string
        labMethodLink:
          type: string
          format: url
          example: "https://doi.org/10.2135/cropsci2017.04.0244"
        labMethodTechnique:
          type: string
          example: "DOI for Beans"
        nutrientAcquisitionDetails:
          type: array
          items:
            $ref: '#/components/schemas/NutrientAcquisitionDetails'
            
    NutrientAcquisitionDetails:
          type: object
          properties:
            sampleUnitId: 
              type: integer
              example: 321632
            purchaseDate:
              type: string
              example: "12/2/2005"
            storeCity:
              type: string
              example: TRUSSVILLE
            storeState:
              type: string
              example: AL
              
    NutrientConversionFactors:
      properties:
        type:
          type: string
          example: ".ProteinConversionFactor"
        value:
          type: number
          format: float
          example: 6.25000000
    FoodUpdateLog:
      properties:
        fdcId:
          type: integer
          example: 534358
        availableDate:
          type: string
          example: "8/18/2018"
        brandOwner:
          type: string
          example: "Kar Nut Products Company"
        dataSource:
          type: string
          example: "LI"
        dataType:
          type: string
          example: "Branded"
        description:
          type: string
          example: "NUT 'N BERRY MIX"
        foodClass:
          type: string
          example: 'Branded'
        gtinUpc:
          type: string
          example: "077034085228"
        householdServingFullText:
          type: string
          example: "1 ONZ"
        ingredients:
          type: string
          example: "PEANUTS (PEANUTS, PEANUT AND/OR SUNFLOWER OIL). RAISINS. DRIED CRANBERRIES (CRANBERRIES, SUGAR, SUNFLOWER OIL). SUNFLOWER KERNELS AND ALMONDS (SUNFLOWER KERNELS AND ALMONDS, PEANUT AND/OR SUNFLOWER OIL)."
        modifiedDate:
          type: string
          example: "8/18/2018"
        publicationDate:
          type: string
          example: "4/1/2019"
        servingSize:
          type: integer
          format: float32
          example: 28
        servingSizeUnit:
          type: string
          example: "g"
        brandedFoodCategory:
          type: string
          example: "Popcorn, Peanuts, Seeds & Related Snacks"
        changes:
          type: string
          example: "Nutrient Added, Nutrient Updated"
        foodAttributes:
          type: array
          items:
            $ref: '#/components/schemas/FoodAttribute'
        
    FoodAttribute:
      properties:
        id:
          type: integer
          example: 25117
        sequenceNumber:
          type: integer
          example: 1
        value:
          type: string
          example: "Moisture change: -5.0%"
        FoodAttributeType:
          type: object
          properties:
            id:
              type: integer
              example: 1002
            name:
              type: string
              example: "Adjustments"
            description:
              type: string
              example: "Adjustments made to foods, including moisture and fat changes."
              
    FoodCategory:
      properties:
        id:
          type: integer
          format: int32
          example: 11
        code:
          type: string
          example: "1100"
        description:
          type: string
          example: "Vegetables and Vegetable Products"
    
    FoodComponent:
      properties:
        id:
          type: integer
          format: int32
          example: 59929
        name:
          type: string
          example: "External fat"
        dataPoints:
          type: integer
          example: 24
        gramWeight:
          type: number
          example: 2.1
        isRefuse:
          type: boolean
          example: true
        minYearAcquired:
          type: integer
          example: 2011
        percentWeight:
          type: number
          example: 0.5
          
    FoodPortion:
      properties:
        id:
          type: integer
          format: int32
          example: 135806
        amount:
          type: number
          format: float
          example: 1
        dataPoints:
          type: integer
          format: int32
          example: 9
        gramWeight:
          type: number
          format: float
          example: 91
        minYearAcquired:
          type: integer
          example: 2011
        modifier:
          type: string
          example: "10205"
        portionDescription:
          type: string
          example: "1 cup"
        sequenceNumber:
          type: integer
          example: 1
        measureUnit:
          $ref: '#/components/schemas/MeasureUnit'
    
    InputFoodFoundation:
      description: applies to Foundation foods. Not all inputFoods will have all fields.
      properties:
        id:
          type: integer
          example: 45551
        foodDescription:
          type: string
          example: Beef, Tenderloin Roast, select, roasted, comp5, lean (34BLTR)
        inputFood:
          $ref: '#/components/schemas/SampleFoodItem'
    
    InputFoodSurvey:
      description: applies to Survey (FNDDS). Not all inputFoods will have all fields.
      properties:
        id:
          type: integer
          example: 18146
        amount:
          type: number
          format: float
          example: 1.5
        foodDescription:
          type: string
          example: "Spices, curry powder"
        ingredientCode:
          type: integer
          example: 2015
        ingredientDescription:
          type: string
          example: "Spices, curry powder"
        ingredientWeight:
          type: number
          format: float
          example: 9.45
        portionCode:
          type: string
          example: "21000"
        portionDescription:
          type: string
          example: "1 tablespoon"
        sequenceNumber:
          type: integer
          example: 6
        surveyFlag:
          type: integer
          example: 0
        unit:
          type: string
          example: "TB"
        inputFood:
          $ref: '#/components/schemas/SurveyFoodItem'
        retentionFactor:
          $ref: '#/components/schemas/RetentionFactor'
          
    MeasureUnit:
      properties:
        id:
          type: integer
          format: int32
          example: 999
        abbreviation:
          type: string
          example: "undetermined"
        name:
          type: string
          example: "undetermined"
          
    RetentionFactor:
      properties:
        id:
          type: integer
          example: 235
        code:
          type: integer
          example: 3460
        description:
          type: string
          example: "VEG, ROOTS, ETC, SAUTEED"
          
    WweiaFoodCategory:
      properties:
        wweiaFoodCategoryCode:
          type: integer
          example: 3002
        wweiaFoodCategoryDescription:
          type: string
          example: "Meat mixed dishes"
              
    FoodsCriteria:
      type: object
      description: JSON for request body of 'foods' POST request. Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified. Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
      properties:
        fdcIds:
          description: List of multiple FDC ID's
          type: array
          minItems: 1
          maxItems: 20
          items:
            type: integer
          example: [534358,373052,616350]
        format:
          description: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
          type: string
          enum:
            - abridged
            - full
        nutrients:
          description: Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned.  If a food does not have any matching nutrients, the food will be returned with an empty foodNutrients element.
          type: array
          minItems: 1
          maxItems: 25
          items:
              type: integer
          example: [203, 204, 205]
    
    FoodListCriteria:
      type: object
      description: JSON for request body of 'list' POST request
      properties:
        dataType: 
          description: Optional. Filter on a specific data type; specify one or more values in an array.
          type: array
          items:
            type: string
            enum:
              - Branded
              - Foundation
              - Survey (FNDDS)
              - SR Legacy
          minItems: 1
          maxItems: 4
          example: ["Foundation","SR Legacy"]
        pageSize:
          description: Optional. Maximum number of results to return for the current page. Default is 50.
          type: integer
          minimum: 1
          maximum: 200
          example: 25
        pageNumber:
          description: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
          type: integer
          example: 2
        sortBy:
          description: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases.
          type: string
          enum:
            - dataType.keyword
            - lowercaseDescription.keyword
            - fdcId
            - publishedDate
        sortOrder:
          description: Optional. The sort direction for the results. Only applicable if sortBy is specified.
          type: string
          enum:
            - asc
            - desc
          
    FoodSearchCriteria:
      type: object
      description: A copy of the criteria that were used in the search.
      properties:
        query:
          description: Search terms to use in the search. The string may also include standard [search operators](https://fdc.nal.usda.gov/help.html#bkmk-2)
          type: string
          example: "Cheddar cheese"
        dataType: 
          description: Optional. Filter on a specific data type; specify one or more values in an array.
          type: array
          items:
            type: string
            enum:
              - Branded
              - Foundation
              - Survey (FNDDS)
              - SR Legacy
          minItems: 1
          maxItems: 4
          example: ["Foundation","SR Legacy"]
        pageSize:
          description: Optional. Maximum number of results to return for the current page. Default is 50.
          type: integer
          minimum: 1
          maximum: 200
          example: 25
        pageNumber:
          description: Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
          type: integer
          example: 2
        sortBy:
          description: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will be dataType and description.keyword will be description in future releases.
          type: string
          enum:
            - dataType.keyword
            - lowercaseDescription.keyword
            - fdcId
            - publishedDate
        sortOrder:
          description: Optional. The sort direction for the results. Only applicable if sortBy is specified.
          type: string
          enum:
            - asc
            - desc
        brandOwner:
          description: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods.
          type: string
          example: "Kar Nut Products Company"
        tradeChannel:
          description: Optional. Filter foods containing any of the specified trade channels.
          type: array
          items:
            type: string
            enum:
              - "CHILD_NUTRITION_FOOD_PROGRAMS"
              - "DRUG"
              - "FOOD_SERVICE"
              - "GROCERY"
              - "MASS_MERCHANDISING"
              - "MILITARY"
              - "ONLINE"
              - "VENDING"
          minItems: 1
          maxItems: 3
          example: [“CHILD_NUTRITION_FOOD_PROGRAMS”, “GROCERY”]
        startDate:
          type: string
          example: "2021-01-01"
          description: "Filter foods published on or after this date. Format: YYYY-MM-DD"
        endDate:
          type: string
          example: "2021-12-30"
          description: "Filter foods published on or before this date. Format: YYYY-MM-DD"
    SearchResult:
      properties:
        foodSearchCriteria:
          $ref: '#/components/schemas/FoodSearchCriteria'
        totalHits:
          description: The total number of foods found matching the search criteria.
          type: integer
          example: 1034
        currentPage:
          description: The current page of results being returned.
          type: integer
        totalPages:
          description: The total number of pages found matching the search criteria.
          type: integer
        foods:
          description: The list of foods found matching the search criteria. See Food Fields below.
          type: array
          items:
            $ref: '#/components/schemas/SearchResultFood'
            
    SearchResultFood:
      type: object
      required:
        - fdcId
        - description
      properties:
        fdcId:
          description: Unique ID of the food.
          type: integer
          example: 45001529
        dataType:
          description: The type of the food data.
          type: string
          example: "Branded"
        description:
          description: The description of the food.
          type: string
          example: "BROCCOLI"
        foodCode:
          description: Any A unique ID identifying the food within FNDDS.
          type: string
        foodNutrients:
          type: array
          items:
            $ref: '#/components/schemas/AbridgedFoodNutrient'
        publicationDate:
          description: Date the item was published to FDC.
          type: string
          example: "4/1/2019"
        scientificName:
          description: The scientific name of the food.
          type: string
        brandOwner:
          description: Brand owner for the food. Only applies to Branded Foods.
          type: string
          example: "Supervalu, Inc."
        gtinUpc:
          description: GTIN or UPC code identifying the food. Only applies to Branded Foods.
          type: string
          example: "041303020937"
        ingredients:
          description: The list of ingredients (as it appears on the product label). Only applies to Branded Foods.
          type: string
        ndbNumber:
          description: Unique number assigned for foundation foods. Only applies to Foundation and SRLegacy Foods.
          type: integer
        additionalDescriptions:
          description: Any additional descriptions of the food.
          type: string
          example: "Coon; sharp cheese; Tillamook; Hoop; Pioneer; New York; Wisconsin; Longhorn"
        allHighlightFields:
          description: allHighlightFields
          type: string
        score: 
          description: Relative score indicating how well the food matches the search criteria.
          type: number
          format: float
