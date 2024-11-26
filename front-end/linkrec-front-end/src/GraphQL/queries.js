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

export const CHECK_EMAIL_EXISTS = gql`
  query CheckEmailExists($email: String!) {
    profileByEmail(email: $email) {
      id
    }
  }
`;
