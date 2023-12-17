import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'

import { createVuetify } from 'vuetify';
import { md1 } from 'vuetify/blueprints';

import { VApp } from 'vuetify/components/VApp';
import { VAppBar } from 'vuetify/components/VAppBar';
import { VMain } from 'vuetify/components/VMain';
import { VToolbar, VToolbarItems } from 'vuetify/components/VToolbar';
import { VContainer, VRow, VCol, VSpacer } from 'vuetify/components/VGrid';
import { VMenu } from 'vuetify/components/VMenu';
import { VList, VListItem, VListSubheader, VListItemTitle } from 'vuetify/components/VList';
import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VForm } from 'vuetify/components/VForm';
import { VTextField } from 'vuetify/components/VTextField'
import { VSelect } from 'vuetify/components/VSelect';
import { VVirtualScroll } from 'vuetify/components/VVirtualScroll';
import { VDivider } from 'vuetify/components/VDivider';
import { VDataTableVirtual } from 'vuetify/components/VDataTable';
import { VBtn } from 'vuetify/components/VBtn';
import { VDialog } from 'vuetify/components/VDialog';
import { VTooltip } from 'vuetify/components/VTooltip';
import { VIcon } from 'vuetify/components/VIcon';


const vuetify = createVuetify({
    blueprint: md1,
    icons: {
        defaultSet: 'mdi',
    },
    components: {
        VApp,
        VAppBar,
        VMain,

        VToolbar,
        VToolbarItems,

        VContainer,
        VRow,
        VCol,
        VSpacer,

        VMenu,

        VList,
        VListItem,
        VListSubheader,
        VListItemTitle,

        VCard,
        VCardTitle,
        VCardText,
        VCardActions,

        VForm,
        VTextField,
        VSelect,

        VVirtualScroll,

        VDivider,

        VDataTableVirtual,

        VBtn,
        VDialog,

        VTooltip,

        VIcon,
    }
});

export default vuetify
