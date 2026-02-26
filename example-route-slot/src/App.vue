<template>
    <DlThemeProvider :is-dark="isDark" class="main-background">
        <div v-if="!isReady" class="loading-spinner">
            <dl-spinner type="clock" text="Loading..." />
        </div>
        <div v-else class="demo-container">
            <div class="demo-card">
                <dl-icon icon="icon-dl-dataloop" size="xl" :svg="true" />
                <dl-typography variant="h2" color="textPrimary">Route Slot Example</dl-typography>
                <dl-typography color="textSecondary">
                    This is a simple route-slot application running in the Dataloop platform.
                </dl-typography>

                <div class="info-section">
                    <div class="info-row">
                        <dl-typography color="textSecondary">User:</dl-typography>
                        <dl-typography color="textPrimary">{{ currentUser }}</dl-typography>
                    </div>
                    <div class="info-row">
                        <dl-typography color="textSecondary">Project ID:</dl-typography>
                        <dl-typography color="textPrimary">{{ projectId }}</dl-typography>
                    </div>
                    <div class="info-row">
                        <dl-typography color="textSecondary">Theme:</dl-typography>
                        <dl-typography color="textPrimary">{{ isDark ? 'Dark' : 'Light' }}</dl-typography>
                    </div>
                </div>

                <div class="actions">
                    <dl-button label="Test Button" @click="handleClick" />
                </div>

                <dl-alert v-if="showMessage" type="info" class="demo-alert" :fluid="true">
                    Button clicked! App is responsive.
                </dl-alert>
            </div>
        </div>
    </DlThemeProvider>
</template>

<script setup lang="ts">
import {
    DlThemeProvider,
    DlSpinner,
    DlButton,
    DlTypography,
    DlIcon,
    DlAlert
} from '@dataloop-ai/components'
import { DlEvent, ThemeType } from '@dataloop-ai/jssdk'
import { ref, onMounted, computed } from 'vue'

const isReady = ref(false)
const currentTheme = ref<ThemeType>(ThemeType.DARK)
const currentUser = ref('')
const projectId = ref('')
const showMessage = ref(false)

const isDark = computed(() => currentTheme.value === ThemeType.DARK)

const handleClick = () => {
    showMessage.value = true
    setTimeout(() => {
        showMessage.value = false
    }, 3000)
}

onMounted(() => {
    window.dl.on(DlEvent.READY, async () => {
        const settings = await window.dl.settings.get()
        currentUser.value = settings.currentUser
        const project = await window.dl.projects.get()
        projectId.value = project.id

        currentTheme.value = settings.theme as unknown as ThemeType
        window.dl.on(DlEvent.THEME, (data) => {
            currentTheme.value = data
        })
        isReady.value = true
    })
})
</script>

<style scoped>
.main-background {
    background-color: var(--dell-white);
}

.loading-spinner {
    display: grid;
    place-items: center;
    height: 100vh;
}

.demo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.demo-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 3rem;
    border-radius: 12px;
    border: 1px solid var(--dell-gray-300);
    background-color: var(--dell-white);
    max-width: 400px;
    width: 100%;
}

.info-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    padding: 1rem;
    border-radius: 8px;
    background-color: var(--dell-gray-100);
    margin-top: 0.5rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.actions {
    margin-top: 0.5rem;
}

.demo-alert {
    width: 100%;
}
</style>
