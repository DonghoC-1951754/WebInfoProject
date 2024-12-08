import { gql } from '@apollo/client';

export const CREATE_USER = gql`
  mutation CreateUser(
    $firstName: String!,
    $name: String!,
    $email: String!,
    $dateOfBirth: Date!,
    $location: LocationInput!,
    $gender: String!,
  ) {
    createUser(
      firstName: $firstName,
      name: $name,
      email: $email,
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
  mutation createCompany(
    $name: String!,
    $email: String!,
    $location: LocationInput!
  ) {
    createCompany(
      name: $name,
      email: $email,
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
    $location: LocationInput,
    $gender: String,
    $lookingForWork: Boolean,
    $skills: [String]
  ) {
    updateUser(
      id: $id,
      firstName: $firstName,
      name: $name,
      location: $location,
      gender: $gender,
      lookingForWork: $lookingForWork,
      skills: $skills
    ) {
      id
      firstName
      name
      gender
      lookingForWork
      skills
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

export const UPDATE_COMPANY = gql`
  mutation UpdateCompany(
    $id: ID!,
    $name: String,
    $location: LocationInput
  ) {
    updateCompany(
      id: $id,
      name: $name,
      location: $location,
    ) {
      id
      name
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

// Add Education to a User
export const ADD_USER_EDUCATION = gql`
  mutation AddUserEducation($userId: ID!, $education: EducationInput!) {
    addUserEducation(userId: $userId, education: $education) {
      id
      institution
      degree
      fieldOfStudy
      yearGraduated
    }
  }
`;

// Update Education of a User
export const UPDATE_USER_EDUCATION = gql`
  mutation UpdateUserEducation(
    $userId: ID!,
    $educationId: ID!,
    $education: EducationInput!
  ) {
    updateUserEducation(userId: $userId, educationId: $educationId, education: $education) {
      id
      institution
      degree
      fieldOfStudy
      yearGraduated
    }
  }
`;

// Remove Education from a User
export const REMOVE_USER_EDUCATION = gql`
  mutation RemoveUserEducation($userId: ID!, $educationId: ID!) {
    removeUserEducation(userId: $userId, educationId: $educationId)
  }
`;

// Add Experience to a User
export const ADD_USER_EXPERIENCE = gql`
  mutation AddUserExperience($userId: ID!, $experience: ExperienceInput!) {
    addUserExperience(userId: $userId, experience: $experience) {
      id
      company {
        id
        name
      }
      jobTitle
      startDate
      endDate
      description
    }
  }
`;

// Update Experience of a User
export const UPDATE_USER_EXPERIENCE = gql`
  mutation UpdateUserExperience(
    $userId: ID!,
    $experienceId: ID!,
    $experience: ExperienceInput!
  ) {
    updateUserExperience(userId: $userId, experienceId: $experienceId, experience: $experience) {
      id
      company {
        id
        name
      }
      jobTitle
      startDate
      endDate
      description
    }
  }
`;

// Remove Experience from a User
export const REMOVE_USER_EXPERIENCE = gql`
  mutation RemoveUserExperience($userId: ID!, $experienceId: ID!) {
    removeUserExperience(userId: $userId, experienceId: $experienceId)
  }
`;

// Mutation to send a connection request
export const SEND_CONNECTION_REQUEST = gql`
  mutation sendConnectionRequest($fromUserId: ID!, $toUserId: ID!) {
    sendConnectionRequest(fromUserId: $fromUserId, toUserId: $toUserId) {
      id
      fromUser {
        id
      }
      toUser {
        id
      }
      status
    }
  }
`;


export const UPDATE_CONNECTION_REQUEST = gql`
  mutation UpdateConnectionRequest($connectionId: ID!, $status: String!) {
    updateConnectionRequest(connectionId: $connectionId, status: $status) {
      id
      fromUser {
        id
      }
      toUser {
        id
      }
      status
    }
  }
`;

export const REMOVE_CONNECTION = gql`
  mutation RemoveConnection($connectionId: ID!) {
    removeConnection(connectionId: $connectionId) 
  }
`;

export const CREATE_VACANCY = gql`
  mutation CreateVacancy($vacancy: VacancyInput!) {
    createVacancy(vacancy: $vacancy) {
      id
      jobTitle
      company {
        id
        name
      }
      requiredSkills
      startDate
      endDate
    }
  }
`;

export const UPDATE_VACANCY = gql`
  mutation UpdateVacancy($id: ID!, $vacancy: VacancyInput!) {
    updateVacancy(id: $id, vacancy: $vacancy) {
      id
      jobTitle
      company {
        id
        name
      }
      requiredSkills
      startDate
      endDate
    }
  }
`;

// Delete a Vacancy
export const DELETE_VACANCY = gql`
  mutation DeleteVacancy($id: ID!) {
    deleteVacancy(id: $id)
  }
`;