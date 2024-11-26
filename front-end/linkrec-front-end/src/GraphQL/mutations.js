import { gql } from '@apollo/client';

export const CREATE_PROFILE = gql`
  mutation CreateProfile($firstName: String!, $name: String!, $email: String!, $location: String!) {
    createProfile(firstName: $firstName, name: $name, email: $email, location: $location) {
      id
      firstName
      name
      email
      location
    }
  }
`;

export const UPDATE_PROFILE = gql`
  mutation UpdateProfile($id: ID!, $firstName: String!, $name: String, $email: String, $location: String) {
    updateProfile(id: $id, firstName: $firstName, name: $name, email: $email, location: $location) {
      id
      firstName
      name
      email
      location
    }
  }
`;
