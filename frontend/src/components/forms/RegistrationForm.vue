<script setup>
import { useForm, useField } from 'vee-validate';

import { authRegistration } from '../../http/requests';
import { EmailValidation, PasswordValidation, NameValidation } from '../../vee-validate/yup'

const emits = defineEmits([
    'beforeRequest',
    'afterResponse',
    'errorRequest',
]);

const { handleSubmit, handleReset } = useForm({
    validationSchema: {
        firstName: NameValidation,
        lastName: NameValidation,
        email: EmailValidation,
        password: PasswordValidation,
    },
});

const firstName = useField('firstName');
const lastName = useField('lastName');
const email = useField('email');
const password = useField('password');

const submit = handleSubmit(async (values) => {
    const formData = new FormData();
    formData.append('first_name', values.firstName);
    formData.append('last_name', values.lastName);
    formData.append('email', values.email);
    formData.append('password', values.password);

    try {
        emits('beforeRequest');
        const response = await authRegistration(formData);
        emits('afterResponse', response);
    }
    catch (error) {
        console.log('Error in RegistrationForm -> submit')
        console.error(error);

        emits('errorRequest');
    }
});
</script>

<template>
    <VCard
    elevation="3"
    width="400"
    heigth="450"
    class="mx-auto"
    >
        <VForm
        @submit="submit"
        class="mx-4 my-4"
        >
            <VTextField
            label="Name"
            v-model="firstName.value.value"
            :error-messages="firstName.errorMessage.value"
            ></VTextField>

            <VTextField
            label="Surname"
            v-model="lastName.value.value"
            :error-messages="lastName.errorMessage.value"
            ></VTextField>

            <VTextField
            label="Email"
            v-model="email.value.value"
            :error-messages="email.errorMessage.value"
            ></VTextField>

            <VTextField
            label="Password"
            v-model="password.value.value"
            :error-messages="password.errorMessage.value"
            ></VTextField>

            <div class="d-flex justify-end">
                <VBtn type="submit">Sign Up</VBtn>
            </div>
        </VForm>
    </VCard>
</template>

<style scope>
</style>
