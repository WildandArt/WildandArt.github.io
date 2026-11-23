# Yad2 Ra'anana / Раанана — пакет данных

**Collection date / дата сбора:** 2026-11-23 (Asia/Jerusalem)  
**Source / источник:** [Yad2 for-sale, Раанана (city=8700)](https://www.yad2.co.il/realestate/forsale/center-and-sharon?area=42&city=8700) — встроенный `__NEXT_DATA__` поисковой выдачи.  
**Scope / объём:** страницы **1–8 из 32** (в выдаче было заявлено 1 275 объявлений; в пакете **313** уникальных).  
**Цены — запрашиваемые (asking prices), не закрытые сделки.**

Этот каталог можно передать другим ботам или людям: CSV + JSON с полной строкой по каждому объявлению, статистика и приблизительные полигоны районов, станции, карусель новостроек, словарь полей.

---

## English

### What’s in the package

| File | What it is |
|---|---|
| `listings.csv` / `listings.json` | One row/object per listing, all fields below (photos, distances, neighborhood stats joined). |
| `neighborhoods.csv` / `neighborhoods.json` | Per-neighborhood counts and medians, plus `polygon_id`. |
| `neighborhoods.geojson` | Approximate neighborhood polygons (Voronoi). `id` / `polygon_id` joins to listings. |
| `city_boundary.geojson` | Official municipal outline: [OSM relation 1383630](https://www.openstreetmap.org/relation/1383630). |
| `stations.json` | Ra'anana West & South railway stations, with Wikipedia source links. |
| `projects.json` | 31 items from the Yad2 “new projects” carousel (not the 313 listings). |
| `meta.json` | Collection metadata, photo counts, limitations. |
| `README.md` | This file. |
| `yad2-raanana-2026-11-23.zip` | Zip of the files above (the zip is not inside itself). |

CSV is **UTF-8 with BOM** (`utf-8-sig`) so Excel opens Hebrew correctly. In CSV, arrays (`photos`, `tags`) are joined with ` | `. JSON keeps real arrays. Booleans in CSV are `true` / `false`.

### Method (short)

- Listings were read from the Yad2 search-feed JSON (`__NEXT_DATA__`), pages 1–8, on 2026-11-23. A Radware/hCaptcha appeared once on page 3 and was solved; pages 4–8 loaded without another challenge. Item pages were **not** opened afterwards.
- `price_per_sqm` = `price / sqm_used`. `sqm_used` prefers Yad2 `squareMeterBuild`, otherwise `squareMeter`. Computed from asking prices on 2026-11-23.
- Coordinates: Yad2 lat/lon for 312 listings; 1 listing geocoded with [Nominatim](https://nominatim.openstreetmap.org/) (1 req/s). `geocode_quality` describes how unique/reliable the point is (see dictionary). Distances to stations are haversine (R = 6371 km).
- Neighborhood polygons: OSM has **place nodes** for most Yad2 names, but **no neighborhood boundary polygons**. Cells are a Voronoi diagram of those nodes (or the listing-coordinate centroid if no node), clipped to the municipal polygon 1383630. Treat them as **approximate, computed**, not official limits.
- Photos: every URL present in the search-feed `images` array (and the cover). The feed gave **at most 4** photos per listing (average **3.29**; 295 of 313 have at least one). Live URLs on `img.yad2.co.il` loaded in a browser on 2026-11-23; they may expire later.
- Sorrento / דירה בהנחה reference: **23,549 ₪/m²** incl. VAT, lottery 2607. Not a row in `listings`. Nominatim returned 0 hits, so there is no map point.
- Year built was **not** in the search feed. “New” is only the Yad2 tags `חדש מקבלן` (new from contractor) and `נכס חדש` (tagged “new property”) — absence of a tag does not mean “old”.

### Limitations

- Asking prices, not deals. Sample is pages 1–8 of 32 (~25% of the then-reported 1,275 ads).
- Polygons are approximate (see above). Four Yad2 names had no OSM node, so the Voronoi seed is a listing centroid: `מרכז דרום`, `קרית שז"ר`, `קזן`, `שאר העיר`. Listings with neighborhood `(לא צוין)` have no polygon (`polygon_id` is empty).
- Some OSM names differ from Yad2 (documented in `osm_note`): e.g. Yad2 `נווה דוד רמז` ↔ OSM `קרית רמז`.
- One listing (`nn6nbp5w`) has 440 ₪/m² (₪39,600 / 90 m²). It is flagged `is_ppm_outlier=true`. Keep it in the table; exclude it from color scales if you draw a choropleth. Another extreme asking price is `5t2mrnje` (222 ₪/m², a house). High ₪/m² values (including plots) are also as published/computed, not corrected.
- Planned Metro M1 station names appear on NTA pages, but **no public coordinates** were found; they are not in `stations.json` and distances to M1 were not computed. NTA Red and Purple light-rail lines do not go through Ra'anana.
- 9 listings have no asking price. 18 listings have no photos in the feed.
- 172 listings share a Yad2 coordinate with at least one other ad (`yad2_coord_share_count` > 1). Some of these are likely building-level or neighborhood centroids, especially when `street` is empty.

### Join keys

- Listing → neighborhood: `polygon_id` (Yad2 neighborhood name / Hebrew key), or `neighborhood_he`.
- Listing → station: `nearest_station` is `west` or `south` (see `stations.json` `id`).
- Listing URL: `https://www.yad2.co.il/realestate/item/{token}`.

### Data dictionary — `listings`

| Field | Type | Meaning |
|---|---|---|
| `token` | string | Yad2 item id. |
| `url` | string | Canonical listing URL. |
| `city` | string | Always רעננה in this file. |
| `neighborhood_he` | string | Yad2 neighborhood name (Hebrew), or `(לא צוין)` if missing. |
| `neighborhood_ru` | string | Russian transliteration of that name. |
| `neighborhood_id` | number/null | Yad2 neighborhood id, when present. |
| `polygon_id` | string/null | Join to `neighborhoods.geojson` / `neighborhoods.csv`. Null when neighborhood was not stated. |
| `street`, `house_number` | string/null | As in the feed. |
| `address_text` | string | Convenience: street + house + neighborhood Hebrew. |
| `floor` | number/null | Floor. |
| `property_type_he` / `property_type_ru` | string | Type in Hebrew (Yad2) and Russian. |
| `rooms` | number/null | Room count (may be half rooms, e.g. 4.5). |
| `sqm` | number/null | Yad2 `squareMeter`. |
| `sqm_build` | number/null | Yad2 `squareMeterBuild`. |
| `sqm_used` | number/null | Denominator actually used for ₪/m². |
| `sqm_used_field` | string/null | `squareMeterBuild` or `squareMeter`. |
| `price` | number/null | Asking price, ₪. |
| `price_per_sqm` | number/null | Computed ₪/m² (rounded as stored from the crawl). |
| `price_before_tag` | number/null | Previous asking price when a drop was shown. |
| `price_drop_abs` | number/null | `price_before_tag - price` when a drop is shown. |
| `price_drop_pct` | number/null | Drop as a percent of `price_before_tag` (1 decimal). |
| `has_price_drop` | boolean | True when a drop is shown. |
| `seller` | string | `agency` or `private`. |
| `agency_name` | string/null | Agency name, if any. |
| `ad_type` | string/null | Feed field (`commercial` / `private`, etc.). |
| `is_asset_exclusive` | boolean | Feed `in_property.isAssetExclusive`. |
| `tags` | list / `\|` | Yad2 tags, e.g. `חדש מקבלן`, `נכס חדש`, `חניה`. |
| `age_flag` | string | `חדש מקבלן`, `נכס חדש`, or `unknown` (no such tag). Not a construction year. |
| `is_new_from_contractor` | boolean | True if tag/flag is `חדש מקבלן`. |
| `year_built` | null | Not present in the search feed. |
| `date_approved` | string/null | Feed `dates.approvedAt` (ISO), only filled for 46 listings. |
| `cover_image` | string/null | Main photo URL. |
| `photos` | list / `\|` | All photo URLs from the feed, cover first. |
| `photo_count` | number | `len(photos)`. |
| `lat`, `lon` | number | Coordinates used on the map and for distances. |
| `lat_yad2`, `lon_yad2` | number/null | Raw Yad2 coordinates. |
| `lat_nominatim`, `lon_nominatim` | number/null | Nominatim result, when a street was queried. |
| `coord_source` | string | `yad2` (312) or `nominatim` (1). |
| `yad2_coord_share_count` | number | How many listings in this file share the exact Yad2 lat/lon. |
| `geocode_quality` | string | See values below. |
| `nominatim_query`, `nominatim_name`, `nominatim_kind` | string/null | Nominatim query and match, when used. |
| `dist_nearest_m` | number | Distance in meters to the nearer of the two stations. |
| `nearest_station` | string | `west` or `south`. |
| `dist_west_m`, `dist_south_m` | number | Distance to each station, m. |
| `dist_band` | string | Band used in the analysis, e.g. `1500–2000 м`. |
| `page` | number | Search-results page (1–8) the ad was taken from. |
| `subcategory_id` | number/null | Yad2 subcategory id. |
| `is_ppm_outlier` | boolean | The 440 ₪/m² listing `nn6nbp5w`. |
| `neigh_*` | number/null | **Joined neighborhood stats** (same values as in `neighborhoods.csv`) so a listing row is comparable on its own. `neigh_med_ppm_apt` is the apartment median ₪/m² of that neighborhood in this sample, etc. |

**`geocode_quality` values**

| Value | Meaning |
|---|---|
| `yad2_unique_street` | Yad2 point, unique in this file, street present. |
| `yad2_unique_no_street` | Yad2 point, unique, no street. |
| `yad2_shared_street` | Same Yad2 point as other ads, street present (often the same building). |
| `yad2_shared_centroid` | Same Yad2 point as other ads, no street (often a neighborhood/city centroid). |
| `nominatim_street` | Map/distance point taken from Nominatim, not the raw Yad2 point. |

### Data dictionary — `neighborhoods`

Counts and medians are computed from **this sample only**. `med_ppm_apt` / `med_price_apt` use property type `דירה`. `*_all` uses every type with a valid price and area. `color_ppm` equals `med_ppm_apt` (null if there is no apartment with ₪/m²). `has_polygon` is false only for `(לא צוין)`. `seed_source` is `osm_node` or `listing_centroid`. OSM columns document the place node used as the Voronoi seed.

### Stations (source links)

- West / Раанана-Запад: 32.18028°N, 34.85083°E — <https://en.wikipedia.org/wiki/Ra%27anana%E2%80%93West_railway_station> (opened 2018-07-03).
- South / Раанана-Юг: 32.17278°N, 34.88750°E — <https://en.wikipedia.org/wiki/Ra%27anana%E2%80%93South_railway_station> (opened 2018-07-03).

### Interactive map

A Leaflet map of this dataset (filters, photo gallery, Street View links, starring) lives next to this package: `../raanana_map.html`. A copy is also included in the zip when packaged together. Open it in a browser **with network access** (OpenStreetMap tiles + Leaflet CDN + Yad2 photo URLs).

---

## Русский

### Что в пакете

Те же файлы, что в таблице выше. `listings.csv` / `listings.json` — полная строка по каждому объявлению (все фото из ленты, координаты и качество геокода, снижение цены, теги, расстояние до ближайшей станции, к строке присоединены медианы района). Полигоны районов — **приблизительные** (Вороной по узлам OSM или центроиду объявлений, обрезка по муниципальной границе [OSM relation 1383630](https://www.openstreetmap.org/relation/1383630)); в OSM полигонов районов Раананы нет, только точки. CSV в UTF-8 с BOM.

### Как собирали и чем это не является

Собрано 23 ноября 2026 (Asia/Jerusalem) из JSON поисковой выдачи Yad2, **страницы 1–8 из 32**. Цены — **предложения, не сделки**. ₪/м² посчитан как цена ÷ площадь (built, иначе указанная). Один раз на 3-й странице был Radware/hCaptcha; страницы карточек объявлений после этого не открывались, поэтому галерея — это то, что было в ленте (не больше 4 фото на объект). Года постройки в ленте нет; «новое» — только метки Yad2 `חדש מקבלן` и `נכס חדש`. Точки Сорренто в OSM/Nominatim нет, в файле только референс **23 549 ₪/м²**. Координат станций метро M1 в открытых источниках НТА нет — в `stations.json` только две действующие ж/д станции (Википедия). Выброс 440 ₪/м² помечен `is_ppm_outlier`.

Словарь полей — в английской части выше (имена колонок те же).


### Amenities / удобства (derived from search-feed tags, 2026-11-23)

The Yad2 *search feed* in this sample did not include structured fields for elevator (מעלית), storage (מחסן), air-con (מיזוג), or property condition. Flags below were computed from the `tags` array (and from property type `דירת גן` for the garden flag). **A missing tag is not proof the amenity is absent.**

| Field | Meaning | True in this sample |
|---|---|---|
| `has_mamad` | Tag `ממ"ד` (safe / mamad room) | 84 |
| `has_parking` | Tag `חניה` | 106 |
| `has_balcony` / `balcony_count` | Tags like `2 מרפסות` | 34 |
| `has_garden` | Property type `דירת גן` (or a garden tag, none in this feed) | 20 |
| `has_elevator`, `has_storage`, `has_aircon` | No such tags in the feed | 0 |
| `air_directions`, `bathroom_count`, `is_rear_facing`, `has_park_view`, `has_city_view` | Parsed from tags when present | — |
| `amenities_source` | Always `yad2_search_feed_tags` | — |


### Rent listings / аренда

Rent crawl of https://www.yad2.co.il/realestate/rent/center-and-sharon?area=42&city=8700 on 2026-11-23 (Asia/Jerusalem) was **stopped on the first request**: the tab landed on Radware Bot Manager Captcha (`validate.perfdrive.com`) and stayed there. The one allowed captcha had already been used earlier the same day on the sale crawl. No rent pages were collected. See `rent_status.json`. Median rent, ₪/m²/month, and gross rental yield were **not computed**.


## Sorrento calculator / калькулятор Сорренто

Self-contained HTML, works under `file://`: `sorrento_calc.html`.

Default inputs (every figure has a source link in the UI):

- Square metres: starting value 100 (an input, not a measured Sorrento size).
- Rooms: 4.
- Price: ₪23,549/m² incl. VAT — דירה בהנחה / Sorrento, lottery 2607 (user-stated programme price). Toggle «without discount»: apartment median ₪31,500/m² from Yad2 for-sale feed, n=177, asking prices, 2026-11-23, pages 1–8 of 32.
- Cash: ₪600,000 (user-stated).
- Mortgage rate: Bank of Israel average effective annual rate on new **unindexed** housing loans, 20–25 year bucket, **4.888%**. Reporting month October 2026, effective from 2026-11-12. File: https://www.boi.org.il/boi_files/Pikuah/mashfix.xls (updated 2026-11-11). Page: https://www.boi.org.il/information/interestrates/mortgage/
- Term: 25 years (editable assumption). Changing the term refills the official bucket rate unless the rate was edited by hand.
- Expected rent: official **nadlan.gov.il** Ra'anana `lastYearAvgPrice` for 4 rooms, ₪6,950/month (data version 20-08-2026). Latest quarter (2026-06) in the same file: ₪7,000. API: https://data.nadlan.gov.il/api/pages/settlement/rent/8700.json
  - 3 rooms: ₪5,800 (latest quarter ₪6,000). 5 rooms: ₪8,600.
  - 2 and 6 rooms: no Ra'anana series in that API; the calculator then prefills **CBS Central District** (not the city) from Table 4.9, Q3 2026.
- Vacancy default 0% and ועד בית default ₪250/month are **editable assumptions**, not official figures.
- Arnona: computed from Ra'anana municipal ordinance 2026, **automatic-update-only** column (the «requested *» column adds 2.4% and requires ministerial approval; not used). Default zone 1 (higher band) is an assumption — Sorrento’s zone was not checked on the ordinance map. 100 m² zone 1 → ₪53.34/m²/year = ₪445/month. PDF: https://www.raanana.muni.il/wp-content/uploads/2025/11/%D7%A6%D7%95-%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94-2026.pdf

Bank of Israel Directive 329 (https://www.boi.org.il/media/uckpqztg/329_et.pdf): max LTV 75% sole dwelling, 70% replacement, 50% investment. Hard PTI cap 50% of disposable income (§ 5). Above 40% PTI the loan gets a 100% risk weight (§ 6) — not a prohibition. Explainer: https://www.boi.org.il/en/information-and-service-to-the-public/banking-customer-service-information/financial-education/the-reform-to-increase-information-transparency-and-competition-in-mortgages/

CBS Table 4.9 does **not** publish Ra'anana (cities above 100,000 only). Latest table: Price Statistics Monthly 10/2026, Q3 2026 (VII–IX). National average rent ₪5,131.8/month (+3.6% vs Q3 2025 ₪4,952.2). Central District ₪5,544.1 (+5.5% vs ₪5,256.7). No separate Sharon rent index. PDFs: https://www.cbs.gov.il/he/publications/Madad/DocLib/2026/price10a/a4_9_h.pdf and `_e.pdf`.

CPI rent index (national): media release 362/2026, 15 Nov 2026, October 2026 CPI. Rent index +0.2% vs September; renewed contracts ≈ +2.8% annual, new tenants ≈ +5.5% annual (official wording: approximation of the annual rate). https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/362/10_26_362e.pdf

Mamad rent premium: Bank of Israel, Yachin & Talmon, March 2025, https://www.boi.org.il/media/egyavnop/n202503h.pdf — asking-rent ads, national, not Ra'anana. Table 1 panel E: pre-war premium 10.49% / 10.43%; after the war started 12.78% / 13.31%. May–Dec 2024 premium was 3.7–4.1 percentage points higher than Jan–Sep 2023. Garden / דירת גן: used only as a property-type dummy; **no published garden rent premium** was found in this paper or in CBS.

Madlan city page returned HTTP 403 (Cloudflare) on 2026-11-23; stopped, no Madlan figures used.

Yad2 rent crawl was not retried (captcha). See `rent_status.json`.

Full source table: `rent_sources.json`.
