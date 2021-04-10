.echo on
.headers on

-- Name: US_States_Covid_Cases_Vaccines_withDemographics.sql
-- Author: Charles Carter
-- Date: April 5, 2021
-- Purpose: Creates table for us_vaccines_with_demographics.csv data file
-- Database: covidproj.db

drop table if exists us_vaccines_with_demographics;

State,week of case date,week of vaccine date,vaccine_date,total_vaccinations,total_distributed,people_vaccinated,people_fully_vaccinated_per_hundred,total_vaccinations_per_hundred,people_fully_vaccinated,people_vaccinated_per_hundred,distributed_per_hundred,daily_vaccinations_raw,daily_vaccinations,daily_vaccinations_per_million,share_doses_used,case_date,cases,deaths,POPULATION,POP_SQMI,POP2010,POP10_SQMI,WHITE,BLACK,AMERI_ES,ASIAN,HAWN_PI,HISPANIC,OTHER,MULT_RACE,MALES,FEMALES,AGE_UNDER5,AGE_5_9,AGE_10_14,AGE_15_19,AGE_20_24,AGE_25_34,AGE_35_44,AGE_45_54,AGE_55_64,AGE_65_74,AGE_75_84,AGE_85_UP,MED_AGE,MED_AGE_M,MED_AGE_F,HOUSEHOLDS,AVE_HH_SZ,HSEHLD_1_M,HSEHLD_1_F,MARHH_CHD,MARHH_NO_C,MHH_CHILD,FHH_CHILD,FAMILIES,AVE_FAM_SZ,HSE_UNITS,VACANT,OWNER_OCC,RENTER_OCC,NO_FARMS12,AVE_SIZE12,CROP_ACR12,AVE_SALE12,SQMI

create table us_vaccines_with_demographics (
    State text,
    week_of_case_date text,
    week_of_vaccine_date text,
    vaccine_date text,
    total_vaccinations integer,
    total_distributed integer,
    people_vaccinated integer,
    people_fully_vaccinated_per_hundred integer,
    total_vaccinations_per_hundred integer,
    people_fully_vaccinated integer,
    people_vaccinated_per_hundred integer,
    distributed_per_hundred integer,
    daily_vaccinations_raw integer,
    daily_vaccinations integer,
    daily_vaccinations_per_million real,
    share_doses_used integer,
    case_date integer,
    cases integer,
    deaths integer,
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
    MED_AGE real,
    MED_AGE_M real,
    MED_AGE_F real,
    HOUSEHOLDS integer,
    AVE_HH_SZ real,
    HSEHLD_1_M integer,
    HSEHLD_1_F integer,
    MARHH_CHD integer,
    MARHH_NO_C integer,
    MHH_CHILD integer,
    FHH_CHILD integer,
    FAMILIES integer,
    AVE_FAM_SZ real,
    HSE_UNITS integer,
    VACANT integer,
    OWNER_OCC integer,
    RENTER_OCC integer,
    NO_FARMS12 integer,
    AVE_SIZE12 real,
    CROP_ACR12 integer,
    AVE_SALE12 real,
    SQMI real
);

.mode csv us_vaccines_with_demographics
.import --skip 1 US_States_Covid_Cases_Vaccines_withDemographics.csv us_vaccines_with_demographics

--drop index if exists us_vaccines_with_demographics_fips_idx;
--create index if not exists us_vaccines_with_demographics_fips_idx on us_vaccines_with_demographics (fips);
--drop index if exists us_vaccines_with_demographics_state_idx;
--create index if not exists us_vaccines_with_demographics_state_idx on us_vaccines_with_demographics (fips);
--drop index if exists us_vaccines_with_demographics_county_idx;
--create index if not exists us_vaccines_with_demographics_county_idx on us_vaccines_with_demographics (fips);

