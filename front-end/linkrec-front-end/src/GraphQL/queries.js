import { gql } from '@apollo/client';

// Fetch all profiles
export const GET_PROFILES = gql`
  query {
    profiles {
      id
      firstName
      name
      email
      location
    }
  }
`;