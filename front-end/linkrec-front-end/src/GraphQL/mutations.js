import { gql } from '@apollo/client';

export const CREATE_USER = gql`
  mutation CreateUser(
    $firstName: String!,
    $name: String!,
    $email: String!,
    $password: String!,
    $dateOfBirth: Date!,
    $location: LocationInput!,
    $gender: String!
  ) {
    createUser(
      firstName: $firstName,
      name: $name,
      email: $email,
      password: $password,
      dateOfBirth: $dateOfBirth,
      location: $location,
      gender: $gender
    ) {
      id
      firstName
      name
      email
      gender
      dateOfBirth
      location {
        country
        city
        cityCode
        street
        houseNumber
      }
    }
  }
`;

export const CREATE_COMPANY = gql`
  mutation CreateUser(
    $name: String!,
    $email: String!,
    $password: String!,
    $location: LocationInput!
  ) {
    createUser(
      name: $name,
      email: $email,
      password: $password,
      location: $location
    ) {
      id
      name
      email
      location {
        country
        city
        cityCode
        street
        houseNumber
      }
    }
  }
`;

export const UPDATE_USER = gql`
  mutation UpdateUser(
    $id: ID!,
    $firstName: String,
    $name: String,
    $email: String,
    $password: String,
    $dateOfBirth: Date,
    $location: LocationInput,
    $gender: String,
    $educations: [EducationInput!],
    $experiences: [ExperienceInput!]
  ) {
    updateUser(
      id: $id,
      firstName: $firstName,
      name: $name,
      email: $email,
      password: $password,
      dateOfBirth: $dateOfBirth,
      location: $location,
      gender: $gender,
      educations: $educations,
      experiences: $experiences
    ) {
      id
      firstName
      name
      email
      gender
      dateOfBirth
      location {
        country
        city
        cityCode
        street
        houseNumber
      }
    }
  }
`;
