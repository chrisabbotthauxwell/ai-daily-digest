// Placeholder so CI has something to build. Real resources arrive in plan 02.
targetScope = 'resourceGroup'

@description('Azure region for all resources.')
param location string = resourceGroup().location

output deployedLocation string = location
