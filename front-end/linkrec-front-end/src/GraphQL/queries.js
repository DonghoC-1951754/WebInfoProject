import { gql } from "@apollo/client";

// Fetch all Users
export const GET_USERS = gql`
  query {
    users {
      id
      firstName
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

export const GET_USER_BY_ID = gql`
  query GetUserById($id: ID!) {
    user(id: $id) {
      id
      firstName
      name
      email
      dateOfBirth
      location {
        country
        city
        cityCode
        street
        houseNumber
      }
      gender
      lookingForWork
      skills
      connections {
        id
        fromUser {
          id
          name
        }
        toUser {
          id
          name
        }
        status
      }
      educations {
        id
        institution
        degree
        fieldOfStudy
        yearGraduated
      }
      experiences {
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
  }
`;

export const GET_COMPANIES = gql`
  query {
    companies {
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


export const GET_COMPANY_BY_ID = gql`
  query GetCompanyById($id: ID!) {
    company(id: $id) {
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
      vacancies {
        id
        jobTitle
        requiredSkills
        startDate
        endDate
      }
    }
  }
`;

export const GET_ACTIVE_VACANCIES = gql`
  query GetActiveVacancies($currentDate: Date!) {
    activeVacancies(currentDate: $currentDate) {
      id
      jobTitle
      company {
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
      requiredSkills
      startDate
      endDate
    }
  }
`;

export const GET_USER_CONNECTIONS = gql`
  query GetUserConnections($userId: ID!, $type: String) {
    connections(userId: $userId, type: $type) {
      id
      fromUser {
        id
        name
      }
      toUser {
        id
        name
      }
      status
    }
  }
`;

export const GET_VACANCIES = gql`
  query GetVacancies {
    vacancies {
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

export const GET_VACANCY_BY_ID = gql`
  query GetVacancyById($id: ID!) {
    vacancy(id: $id) {
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

export const GET_MATCHING_VACANCIES = gql`
  query GetMatchingVacancies($userId: ID!, $currentDate: Date!) {
    matchingVacancies(userId: $userId, currentDate: $currentDate) {
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

export const GET_MATCHED_USERS = gql`
  query GetMatchedUsers($vacancyId: ID!) {
    matchedUsers(vacancyId: $vacancyId) {
      id
      firstName
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

export const GET_COMPANY_VACANCIES = gql`
  query GetCompanyVacancies($companyId: ID!) {
    companyVacancies(companyId: $companyId) {
      id
      jobTitle
      requiredSkills
      startDate
      endDate
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
