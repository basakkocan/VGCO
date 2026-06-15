# Ontology Requirements Specification Document (ORSD) - VGCO v3

**Author(s):** Utku Emre Doğanbaş, Başak Koçan, Gürkan İsmet Arslan, Tarık Aydın  
**Creation Date:** April 26, 2026  
**Modification Date:** June 14, 2026  
**Project:** Video Game Catalog Ontology (VGCO)  

---

## 1. Purpose
The purpose of the Video Game Catalog Ontology (VGCO) is to provide a structured knowledge model for describing and querying video games and their associated metadata. The ontology captures essential information about games, including their genres, platforms, developers, publishers, storefronts, and media assets, so that users can search, filter, and discover games according to various criteria.

## 2. Scope
The focus of the ontology is the `VideoGame` class as a central entity and its direct metadata relationships. 

The ontology covers:
- **Video Games & Descriptive Attributes**: title, description, release date, ESRB ratings, playtime hours, and review scores (user ratings and Metacritic).
- **Relational Associations**: developers, publishers, game series/franchises, and digital/retail distribution storefronts.
- **Media Assets**: URLs pointing to screenshots, trailers, and cover images.
- **Categorization**: gameplay genres and community/store tags.

The ontology does not aim to model detailed real-time player telemetry, in-game characters, or deep gameplay mechanics (e.g. detailed skill trees).

## 3. Implementation Language
Ontology Web Language (OWL), serialized in Turtle (`.ttl`) format.

## 4. Intended End-Users
- **Gamers**: looking to discover new games based on specific criteria (e.g. Metacritic scores, genre preferences, platform availability, multiplayer support, or franchises).
- **Developers & Researchers**: building recommendation engines, game catalog databases, or entertainment knowledge graphs.
- **Ontology Engineers**: seeking to align or extend the model with broader BFO-based or entertainment domain models.

## 5. Intended Uses
1. Searching for games that match specific genre preferences (e.g., all RPG or FPS games).
2. Filtering games by platform availability (e.g., games available on PC and PlayStation).
3. Discovering all games developed or published by a specific studio.
4. Identifying games sold on specific storefronts (e.g., Steam and Epic Games).
5. Querying games based on review scores, Metacritic ratings, or playtime hours.
6. Fetching URLs for trailers and screenshots for specific titles.
7. Filtering by ESRB ratings (e.g., Mature 17+).
8. Discovering if a game is part of a larger franchise or series.
9. Enabling natural language question answering by translating user queries into SPARQL through LLM integration.

## 6. Ontology Requirements

### a. Non-Functional Requirements
- **NFR1 (Multilingual Support)**: The ontology must support English. All classes and properties must include `rdfs:label` and `rdfs:comment` annotations with `@en` language tags.
- **NFR2 (Serialization)**: The ontology must be serialized in OWL/Turtle (`.ttl`) format.
- **NFR3 (Interoperability)**: Existing vocabularies such as Schema.org, DBpedia Ontology, and Wikidata properties should be evaluated and aligned where appropriate to maximize interoperability.

### b. Functional Requirements (Competency Questions)
The functional requirements are formulated as Competency Questions (CQs) that the ontology must be able to answer:

* **CQ1**: Which games belong to a specific genre (e.g., all RPG or FPS games)?
* **CQ2**: On which platforms is a given game available?
* **CQ3**: Which games were developed or published by a specific studio?
* **CQ4**: Which games have a specific ESRB rating?
* **CQ5**: What are the official websites and cover images for a given game?
* **CQ6**: Which games belong to the same genre as a selected game?
* **CQ7**: Which developers have published/developed games on multiple platforms?
* **CQ8**: Which digital stores sell a specific game?
* **CQ9**: What is the Metacritic score or average user rating of a given game?
* **CQ10**: Which games belong to a specific game series or franchise?
* **CQ11**: What screenshots or trailers are available for a given game?

---

## 7. Pre-Glossary of Terms

### a. Terms from Competency Questions
game, genre, platform, developer, publisher, ESRB rating, image, studio, store, score, rating, playtime, series, franchise, screenshot, trailer

### b. Terms from Answers (Ontology Vocabulary)

#### Classes
- `VideoGame`: Represents the interactive software application.
- `Genre`: Gameplay interaction categories (e.g., RPG, Shooter).
- `Platform`: Hardware or operating environments (e.g., PC, PlayStation 5).
- `Developer`: Studios responsible for coding and game design.
- `Publisher`: Entities handling funding, marketing, and distribution.
- `ESRBRating`: Rating category assigned by the ESRB (e.g. Mature17Plus).
- `Store`: Digital or retail storefronts (e.g. Steam).
- `GameSeries`: Overarching franchises (e.g. SoulsSeries).
- `Media`: Abstract class for visual/audial assets.
- `Screenshot` (subclass of `Media`): Gameplay images.
- `Trailer` (subclass of `Media`): Promotional videos.

#### Object Properties
- `availableOn` (VideoGame $\rightarrow$ Platform)
- `developedBy` (VideoGame $\rightarrow$ Developer)
- `publishedBy` (VideoGame $\rightarrow$ Publisher)
- `hasGenre` (VideoGame $\rightarrow$ Genre)
- `hasESRBRating` (VideoGame $\rightarrow$ ESRBRating)
- `soldOn` (VideoGame $\rightarrow$ Store)
- `partOfSeries` (VideoGame $\rightarrow$ GameSeries)
- `hasScreenshot` (VideoGame $\rightarrow$ Screenshot)
- `hasTrailer` (VideoGame $\rightarrow$ Trailer)
- `hasReviewScore` (VideoGame $\rightarrow$ ReviewScore)

#### Datatype Properties
- `title` (VideoGame $\rightarrow$ `xsd:string`)
- `description` (VideoGame $\rightarrow$ `xsd:string`)
- `officialWebsite` (VideoGame $\rightarrow$ `xsd:anyURI`)
- `coverImageUrl` (VideoGame $\rightarrow$ `xsd:anyURI`)
- `mediaUrl` (Media $\rightarrow$ `xsd:anyURI`)
- `releaseDate` (VideoGame $\rightarrow$ `xsd:dateTime`)
- `metacriticScore` (VideoGame $\rightarrow$ `xsd:integer`)
- `rating` (VideoGame $\rightarrow$ `xsd:decimal`)
- `playtimeHours` (VideoGame $\rightarrow$ `xsd:integer`)
- `scoreValue` (ReviewScore $\rightarrow$ `xsd:decimal`)
- `slug` (VideoGame $\rightarrow$ `xsd:string`)

### c. Objects (Key Individuals)
- **Genres**: `RPG`, `Adventure`, `ActionRPG`
- **Platforms**: `PC`, `PlayStation5`, `XboxSeriesX`
- **Organizations**: `LarianStudios`, `FromSoftware`, `BandaiNamco`
- **Stores**: `Steam`, `PlayStationStore`
- **Game Series**: `SoulsSeries`
- **Games**: `TheWitcher3`, `EldenRing`, `Minecraft`, `BaldursGate3`
