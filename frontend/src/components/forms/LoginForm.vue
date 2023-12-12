<script setup>
import { useForm, useField } from 'vee-validate';

import { EmailValidation, PasswordValidation } from '../../vee-validate/yup'
import { authLogin } from '../../http/requests';

const emits = defineEmits([
    'beforeRequest',
    'afterResponse',
    'errorRequest',
]);

const { handleSubmit } = useForm({
    validationSchema: {
        email: EmailValidation,
        password: PasswordValidation,
    },
});

const email = useField('email');
const password = useField('password');

const submit = handleSubmit(async (values) => {
    // alert(`Form was submited.\nValues: ${JSON.stringify(values, null, 4)}`)


    const formData = new FormData();
    formData.append('email', values.email);
    formData.append('password', values.password);

    try {
        emits('beforeRequest');
        const response = await authLogin(formData);
        emits('afterResponse', response);
    }
    catch (error) {
        emits('errorRequest', error);
    }
});
</script>

<template>
    <VCard
    elevation="3"
    width="400"
    height="225"
    class="mx-auto"
    >
        <VForm
        @submit="submit"
        class="mx-4 my-4"
        >
            <VTextField
            label="Email"
            v-model=email.value.value
            :error-messages="email.errorMessage.value"
            ></VTextField>

            <VTextField
            label="Password"
            type="password"
            v-model=password.value.value
            :error-messages="password.errorMessage.value"
            ></VTextField>

            <div class="d-flex justify-end">
                <VBtn type="submit">Sign In</VBtn>
            </div>
        </VForm>
    </VCard>
</template>

<style scope>
</style>
