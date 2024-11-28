import { gql } from '@apollo/client';

export const CREATE_PROFILE = gql`
  mutation CreateProfile(
    $firstName: String!,
    $name: String!,
    $email: String!,
    $password: String!,
    $dateOfBirth: Date!,
    $location: LocationInput!,
    $gender: String!
  ) {
    createProfile(
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

export const UPDATE_PROFILE = gql`
  mutation UpdateProfile(
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
    updateProfile(
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
