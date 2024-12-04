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

export const GET_COMPANIES = gql`
  query {
    users {
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


export const CHECK_USER_EMAIL_EXISTS = gql`
  query CheckUserEmailExists($email: String!) {
    userByEmail(email: $email) {
      id
    }
  }
`;

export const CHECK_COMPANY_EMAIL_EXISTS = gql`
  query CheckCompanyEmailExists($email: String!) {
    companyByEmail(email: $email) {
      id
    }
  }
`;

export const GET_ACTIVE_VACANCIES = gql`
  query GetActiveVacancies($currentDate: Date!) {
    activeVacancies(currentDate: $currentDate) {
      id
      jobTitle
      company {
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
