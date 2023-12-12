<script setup>
import { useForm, useField } from 'vee-validate';
import { EmailValidation, PasswordValidation, NameValidation } from '../../vee-validate/yup'

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

const submit = handleSubmit((values) => {
    alert(1`Registration submit!\n\nValues: ${values}`);
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
