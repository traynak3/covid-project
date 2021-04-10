.echo on
.headers on

-- Name: arcgis-counties.sql
-- Author: Charles Carter
-- Date: April 5, 2021
-- Purpose: Creates table for arcgis.csv data file
-- Database: covidproj.db

drop table if exists arcgis_counties;

create table arcgis_counties (
    ID integer,
    OBJECTID integer,
    NAME text,
    STATE_NAME text,
    STATE_FIPS integer,
    CNTY_FIPS integer,
    FIPS integer,
    POPULATION integer,
    POP_SQMI real,
    POP2010 integer,
    POP10_SQMI real,
    WHITE integer,
    BLACK integer,
    AMERI_ES integer,
    ASIAN integer,
    HAWN_PI integer,
    HISPANIC integer,
    OTHER integer,
    MULT_RACE integer,
    MALES integer,
    FEMALES integer,
    AGE_UNDER5 integer,
    AGE_5_9 integer,
    AGE_10_14 integer,
    AGE_15_19 integer,
    AGE_20_24 integer,
    AGE_25_34 integer,
    AGE_35_44 integer,
    AGE_45_54 integer,
    AGE_55_64 integer,
    AGE_65_74 integer,
    AGE_75_84 integer,
    AGE_85_UP integer,
    MED_AGE integer,
    MED_AGE_M integer,
    MED_AGE_F integer,
    HOUSEHOLDS integer,
    AVE_HH_SZ integer,
    HSEHLD_1_M integer,
    HSEHLD_1_F integer,
    MARHH_CHD integer,
    MARHH_NO_C integer,
    MHH_CHILD integer,
    FHH_CHILD integer,
    FAMILIES integer,
    AVE_FAM_SZ integer,
    HSE_UNITS integer,
    VACANT integer,
    OWNER_OCC integer,
    RENTER_OCC integer,
    NO_FARMS12 integer,
    AVE_SIZE12 integer,
    CROP_ACR12 integer,
    AVE_SALE12 integer,
    SQMI real,
    Shape_Leng real,
    SHAPE_Length real,
    SHAPE_Area real
);

.mode csv arcgis_counties
.import --skip 1 arcgis-USA_Counties.csv arcgis_counties

drop index if exists arcgis_counties_fips_idx;
create index if not exists arcgis_counties_fips_idx on arcgis_counties (fips);
drop index if exists arcgis_counties_state_idx;
create index if not exists arcgis_counties_state_idx on arcgis_counties (fips);
drop index if exists arcgis_counties_county_idx;
create index if not exists arcgis_counties_county_idx on arcgis_counties (fips);
