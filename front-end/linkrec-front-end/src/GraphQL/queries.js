import { gql } from '@apollo/client';

// Fetch all profiles
export const GET_PROFILES = gql`
  query GetProfiles {
    profiles {
      id
      firstName
      name
      email
      location
    }
  }
`;