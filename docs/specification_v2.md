# Ontology Requirements Specification Document (ORSD) v2

## Project Information

**Authors:** Utku Emre Doğanbaş, Başak Koçan, Gürkan İsmet Arslan, Tarık Aydın

**Creation Date:** April 26, 2026

**Modification Date:** May 11, 2026

**Project:** Video Game Catalog Ontology (VGCO)

---

## 1. Purpose

The purpose of the Video Game Catalog Ontology (VGCO) is to provide a structured knowledge model for describing and querying video games and their associated metadata. The ontology captures essential information about games, including their genres, platforms, developers, publishers, and media assets so that users can search and filter games according to various criteria.

---

## 2. Scope

The focus of the ontology is the **VideoGame** as a central entity and its direct metadata relationships.

The ontology covers:

* Video games and their descriptive attributes

  * title
  * description
  * release date
  * ESRB ratings
  * review scores
* Associations

  * developers
  * publishers
  * game series
  * distribution stores
* Media

  * screenshots
  * trailers
  * cover images
* Categorization

  * genres
  * community/store tags

The ontology does **not** aim to model:

* Detailed gameplay mechanics
* In-game characters
* Real-time player data

---

## 3. Implementation Language

* OWL (Web Ontology Language)
* Turtle Serialization (`.ttl`)

---

## 4. Intended End Users

### Gamers

Users looking to discover games based on specific criteria such as genre, platform, ESRB rating, or review scores.

### Developers and Researchers

Researchers and developers building recommendation systems, semantic search applications, or knowledge graphs.

### Ontology Engineers

Researchers seeking to align or extend VGCO with broader ontology frameworks such as BFO.

---

## 5. Intended Uses

1. Searching for games that match specific genre preferences.
2. Filtering games by platform availability.
3. Discovering all games developed or published by a specific studio.
4. Identifying games sold on specific digital stores.
5. Querying games based on review scores, Metacritic ratings, or playtime hours.
6. Fetching URLs for trailers and screenshots.
7. Filtering by ESRB ratings.
8. Discovering whether a game belongs to a larger franchise or series.
9. Supporting natural language question answering through LLM-to-SPARQL translation.

---

## 6. Ontology Requirements

### Non-Functional Requirements

#### NFR1

The ontology must support English. All classes and properties must include `rdfs:label` and `rdfs:comment` annotations using the `@en` language tag.

#### NFR2

The ontology must be serialized in OWL/Turtle (`.ttl`) format.

#### NFR3

Existing vocabularies such as Schema.org, DBpedia Ontology, and Wikidata properties should be evaluated and reused whenever appropriate.

---

### Functional Requirements (Competency Questions)

#### CQ1

Which games belong to a specific genre (e.g., RPG or FPS)?

#### CQ2

On which platforms is a given game available?

#### CQ3

Which games were developed or published by a specific studio?

#### CQ4

Which games have a specific ESRB rating?

#### CQ5

What are the official websites and cover images for a given game?

#### CQ6

Which games belong to the same genre as a selected game?

#### CQ7

Which developers have published games on multiple platforms?

#### CQ8

Which digital stores sell a specific game?

---

## 7. Pre-Glossary of Terms

### Terms from Competency Questions

* Game
* Genre
* Platform
* Developer
* Publisher
* ESRB Rating
* Image
* Studio
* Store

### Terms from Answers

#### Classes

* VideoGame
* Genre
* Platform
* Developer
* Publisher
* ESRBRating
* Screenshot
* Trailer
* Store

#### Data Properties

* title
* officialWebsite
* coverImageUrl
* mediaUrl

#### Object Properties

* hasGenre
* availableOn
* developedBy
* publishedBy
* hasESRBRating
* hasScreenshot

### Example Individuals

#### Genres

* RPG
* Adventure
* ActionRPG

#### Platforms

* PC
* PlayStation5
* XboxSeriesX
* NintendoSwitch

#### Organizations

* LarianStudios
* FromSoftware
* BandaiNamco

#### Stores

* Steam
* PlayStationStore

#### Video Games

* The Witcher 3
* Elden Ring
* Minecraft

---

## Version History

### Version 1

Initial VGCO ontology with core classes:

* VideoGame
* Genre
* Platform
* Developer
* Publisher

### Version 2

Added:

* Store
* GameSeries
* ESRBRating
* Screenshot
* Trailer
* ReviewScore
* RAWG API data acquisition strategy
* LLM-based question answering support
* Extended competency questions
