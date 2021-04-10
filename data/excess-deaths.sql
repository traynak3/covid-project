.echo on
.headers on

-- Name: excess-deaths.sql
-- Author: Charles Carter
-- Date: April 7, 2021
-- Purpose: Creates table for excess-deaths.csv data file
-- Database: covidproj.db

drop table if exists excess_deaths;

--country,placename,frequency,start_date,end_date,year,month,week,deaths,expected_deaths,excess_deaths,baseline

create table excess_deaths (
    country text,
    placename text,
    frequency text,
    start_date text,
    end_date text,
    year integer,
    month integer,
    week integer,
    deaths integer,
    expected_deaths integer,
    excess_deaths integer,
    baseline text
);

.mode csv excess_deaths
.import --skip 1 excess-deaths.csv excess_deaths

drop index if exists start_date_idx;
create index if not exists start_date_idx on excess_deaths(start_date);
drop index if exists end_date_idx;
create index if not exists end_date_idx on excess_deaths(end_date);
