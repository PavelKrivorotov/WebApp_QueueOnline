import { string } from 'yup'


export const EmailValidation = string()
    .required()

export const PasswordValidation = string()
    .min(4)
    .max(128)
    .required()

export const NameValidation = string()
    .max(150)
    .required()
