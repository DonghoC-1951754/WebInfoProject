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
      educations {
        institution
        degree
        fieldOfStudy
        yearGraduated
      }
      experiences {
        company {
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
