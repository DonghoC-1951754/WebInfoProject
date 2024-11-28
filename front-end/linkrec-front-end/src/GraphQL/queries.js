import { gql } from '@apollo/client';

// Fetch all Users
export const GET_USERS = gql`
  query {
    users {
      id
      firstName
      name
      email
      location{
        country
        city
        cityCode
        street
        houseNumber
      }
    }
  }
`;

export const CHECK_EMAIL_EXISTS = gql`
  query CheckEmailExists($email: String!) {
    userByEmail(email: $email) {
      id
    }
  }
`;
