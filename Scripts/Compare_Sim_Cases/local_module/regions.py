#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 22:33:02 2021

@author: glenn
"""

#%%

phu_codes = {
    2226 : 'Algoma Public Health Unit',
    2227 : 'Brant County Health Unit' ,
    2240 : 'Chatham-Kent Health Unit',
    2230 : 'Durham Region Health Department',
    2258 : 'Eastern Ontario Health Unit',
    2233 : 'Grey Bruce Health Unit',
    2234 : 'Haldimand-Norfolk Health Unit',
    2235 : 'Haliburton, Kawartha, Pine Ridge District Health Unit',
    2236 : 'Halton Region Health Department',
    2237 : 'Hamilton Public Health Services',
    2238 : 'Hastings and Prince Edward Counties Health Unit',
    5183 : 'Huron Perth Health Unit',
    2241 : 'Kingston, Frontenac and Lennox and Addington Health Unit',
    2242 : 'Lambton Public Health',
    2243 : 'Leeds, Grenville and Lanark District Health Unit',
    2244 : 'Middlesex-London Health Unit', 
    2246 : 'Niagara Region Public Health Department', 
    2247 : 'North Bay Parry Sound District Health Unit',
    2249 : 'Northwestern Health Unit',
    2251 : 'Ottawa Public Health',
    2253 : 'Peel Public Health',
    2255 : 'Peterborough Public Health',
    2256 : 'Porcupine Health Unit',
    2265 : 'Region of Waterloo, Public Health',
    2257 : 'Renfrew County and District Health Unit',
    2260 : 'Simcoe Muskoka District Health Unit',
    4913 : 'Southwestern Public Health',
    2261 : 'Sudbury and District Health Unit', 
    2262 : 'Thunder Bay District Health Unit', 
    2263 : 'Timiskaming Health Unit', 
    3895 : 'Toronto Public Health',
    2266 : 'Wellington-Dufferin-Guelph Health Unit',
    2268 : 'Windsor-Essex County Health Unit', 
    2270 : 'York Region Public Health'
    }

phu_dict = {
    'GreyBruceHealthUnit' : 'GreyBruce',
    'HuronPerthHealthUnit' : 'HuronPerth',
    'Middlesex-LondonHealthUnit' : 'Middlesex',
    'SouthwesternPublicHealth' : 'Southwestern',
    'LambtonPublicHealth' : 'Lambton',
    'Chatham-KentHealthUnit' : 'Chatham',
    'Windsor-EssexCountyHealthUnit' : 'Windsor',
    'Wellington-Dufferin-GuelphHealthUnit' : 'Wellington',
    'HaltonRegionHealthDepartment' : 'Halton',
    'RegionofWaterlooPublicHealth' : 'Waterloo',
    'HamiltonPublicHealthServices' : 'Hamilton',
    'NiagaraRegionPublicHealthDepartment' : 'Niagara',
    'BrantCountyHealthUnit' : 'Brant',
    'Haldimand-NorfolkHealthUnit' : 'Haldimand',
    'PeelPublicHealth' : 'Peel',
    'YorkRegionPublicHealth' : 'York',
    'TorontoPublicHealth' : 'Toronto',
    'SimcoeMuskokaDistrictHealthUnit' : 'Simcoe',
    'DurhamRegionHealthDepartment' : 'Durham',
    'HaliburtonKawarthaPineRidgeDistrictHealthUnit' : 'Haliburton',
    'PeterboroughPublicHealth' : 'Peterborough',
    'RenfrewCountyandDistrictHealthUnit' : 'Renfrew',
    'HastingsandPrinceEdwardCountiesHealthUnit' : 'Hastings',
    'KingstonFrontenacandLennoxandAddingtonHealthUnit' : 'KFLA',
    'LeedsGrenvilleandLanarkDistrictHealthUnit' : 'Leeds',
    'OttawaPublicHealth' : 'Ottawa',
    'EasternOntarioHealthUnit' : 'Eastern',
    'NorthBayParrySoundDistrictHealthUnit' : 'NorthBay',
    'TimiskamingHealthUnit' : 'Timiskaming',
    'SudburyandDistrictHealthUnit' : 'Sudbury',
    'AlgomaPublicHealthUnit' : 'Algoma',
    'PorcupineHealthUnit' : 'Porcupine',
    'ThunderBayDistrictHealthUnit' : 'ThunderBay',
    'NorthwesternHealthUnit' : 'Northwestern'
}

sw_regions = [
    'GreyBruceHealthUnit',
    'HuronPerthHealthUnit',
    'Middlesex-LondonHealthUnit',
    'SouthwesternPublicHealth',
    'LambtonPublicHealth',
    'Chatham-KentHealthUnit',
    'Windsor-EssexCountyHealthUnit']

cw_regions = [
    'Wellington-Dufferin-GuelphHealthUnit',
    'HaltonRegionHealthDepartment',
    'RegionofWaterlooPublicHealth',
    'HamiltonPublicHealthServices',
    'NiagaraRegionPublicHealthDepartment',
    'BrantCountyHealthUnit',
    'Haldimand-NorfolkHealthUnit']

ce_regions = [
    'PeelPublicHealth',
    'YorkRegionPublicHealth',
    'TorontoPublicHealth',
    'SimcoeMuskokaDistrictHealthUnit',
    'DurhamRegionHealthDepartment',
    'HaliburtonKawarthaPineRidgeDistrictHealthUnit',
    'PeterboroughPublicHealth']

e_regions = [
    'RenfrewCountyandDistrictHealthUnit',
    'HastingsandPrinceEdwardCountiesHealthUnit',
    'KingstonFrontenacandLennoxandAddingtonHealthUnit',
    'LeedsGrenvilleandLanarkDistrictHealthUnit',
    'OttawaPublicHealth',
    'EasternOntarioHealthUnit']

n_regions = [
    'NorthBayParrySoundDistrictHealthUnit',
    'TimiskamingHealthUnit',
    'SudburyandDistrictHealthUnit',
    'AlgomaPublicHealthUnit',
    'PorcupineHealthUnit',
    'ThunderBayDistrictHealthUnit',
    'NorthwesternHealthUnit']

