<template>
  <DlThemeProvider :is-dark="isDark">
    <div id="app">
      <div id="mainContent">
        <h2>Model Training Configuration</h2>

        <!-- Message Display -->
        <DlAlert
          v-if="showMessageBox"
          v-model="showMessageBox"
          :type="messageType"
          :text="messageText"
          closable
          fluid
          class="margin-alert"
        />

        <!-- Model Selection -->
        <section>
          <h3>Select Model</h3>
          <DlSelect
            id="modelSelect"
            v-model="selectedModelId"
            :options="modelSelectOptions"
            :disabled="loadingModels || loadingModel || saving"
            :placeholder="modelSelectPlaceholder"
            emit-value
            searchable
            @update:model-value="onModelSelected"
          />
          <DlAlert
            v-if="!!selectedModel"
            type="info"
            fluid
            :closable="false"
            class="margin-alert"
          >
            <strong>{{ selectedModel?.name }}:</strong>
            {{ selectedModel?.description }}
            <template v-if="selectedModel?.created_at">
              <br />
              <small>
                Created:
                {{ new Date(selectedModel.created_at).toLocaleDateString() }}
              </small>
            </template>
          </DlAlert>
        </section>

        <!-- Configuration Form -->
        <section id="configSection" v-show="!!selectedModel">
          <h3>Model Configuration</h3>

          <!-- Model Name Section -->
          <div id="modelNameSection" class="form-group">
            <DlInput
              id="modelNameInput"
              v-model="modelName"
              title="Model Name"
              placeholder="Enter model name"
              :disabled="saving"
              @input="onModelNameChange"
            />
            <div
              style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 5px;
              "
            >
              <span
                id="cloneIndicator"
                v-show="isCloning"
                style="color: var(--dl-color-info); font-size: 12px"
              >
                ✓ Will create new model
              </span>
            </div>
            <div
              id="modelNameHelp"
              style="
                font-size: 12px;
                color: var(--dl-color-medium);
                margin-top: 4px;
              "
            >
              {{
                isCloning
                  ? "A new model will be created with this configuration"
                  : "Edit the name to clone this model with a new configuration"
              }}
            </div>
          </div>

          <h3>Training Parameters</h3>
          <div id="configForm">
            <!-- Basic Parameters -->
            <div
              class="form-group"
              v-for="field in basicFields"
              :key="field.name"
            >
              <template v-if="field.type === 'checkbox'">
                <DlCheckbox
                  :id="field.name"
                  v-model="formValues[field.name]"
                  :label="field.label"
                  :disabled="saving"
                />
              </template>
              <template v-else-if="field.type === 'number'">
                <DlInput
                  :id="field.name"
                  v-model="formValues[field.name]"
                  :title="field.label"
                  type="number"
                  :disabled="saving"
                />
              </template>
              <template v-else-if="field.type === 'object'">
                <div class="json-editor-wrapper">
                  <label :for="field.name">{{ field.label }}</label>
                  <DlJsonEditor
                    :id="field.name"
                    v-model="formValues[field.name]"
                    :readonly="saving"
                  />
                </div>
              </template>
              <template v-else>
                <DlInput
                  :id="field.name"
                  v-model="formValues[field.name]"
                  :title="field.label"
                  type="text"
                  :disabled="saving"
                />
              </template>
            </div>

            <!-- Advanced Options -->
            <DlAccordion
              v-if="advancedFields.length > 0"
              title="Advanced Options"
              :default-opened="false"
            >
              <div id="advancedForm">
                <div
                  class="form-group"
                  v-for="field in advancedFields"
                  :key="field.name"
                >
                  <template v-if="field.type === 'checkbox'">
                    <DlCheckbox
                      :id="field.name"
                      v-model="formValues[field.name]"
                      :label="field.label"
                      :disabled="saving"
                    />
                  </template>
                  <template v-else-if="field.type === 'number'">
                    <DlInput
                      :id="field.name"
                      v-model="formValues[field.name]"
                      :title="field.label"
                      type="number"
                      :disabled="saving"
                    />
                  </template>
                  <template v-else-if="field.type === 'object'">
                    <div class="json-editor-wrapper">
                      <label :for="field.name">{{ field.label }}</label>
                      <DlJsonEditor
                        :id="field.name"
                        v-model="formValues[field.name]"
                        :readonly="saving"
                      />
                    </div>
                  </template>
                  <template v-else>
                    <DlInput
                      :id="field.name"
                      v-model="formValues[field.name]"
                      :title="field.label"
                      type="text"
                      :disabled="saving"
                    />
                  </template>
                </div>
              </div>
            </DlAccordion>
          </div>
        </section>
      </div>

      <!-- Actions -->
      <div class="actions">
        <div class="actions-left">
          <DlButton
            :disabled="saving || !selectedModel || !modelName"
            :label="saving ? 'Saving...' : buttonText"
            :icon="saving ? 'icon-dl-loading' : null"
            color="dl-color-secondary"
            @click="onSaveButtonClick"
          />
        </div>
        <div class="actions-right">
          <DlButton label="Close" outlined :disabled="saving" @click="cancel" />
        </div>
      </div>
    </div>
  </DlThemeProvider>
</template>

<script setup lang="ts">
import {
  DlThemeProvider,
  DlSelect,
  DlAlert,
  DlButton,
  DlCheckbox,
  DlInput,
  DlAccordion,
  DlJsonEditor,
} from "@dataloop-ai/components";
import { DlEvent, ThemeType } from "@dataloop-ai/jssdk";
import { ref, onMounted, computed, watch, nextTick } from "vue-demi";

type MessageType = "info" | "success" | "error" | "warning";
type FieldType = "checkbox" | "number" | "text" | "object";

interface FieldDef {
  name: string;
  label: string;
  type: FieldType;
  default: any;
}

const currentTheme = ref<ThemeType>(ThemeType.LIGHT);
const isDark = computed<boolean>(() => currentTheme.value === ThemeType.DARK);

const API_BASE = window.location.origin + "/api";

// Context/state
const currentProject = ref<any | null>(null);
const availableModels = ref<any[]>([]);
const selectedModel = ref<any | null>(null);
const selectedModelId = ref<string>("");
const originalModelName = ref<string | null>(null);
const isCloning = ref<boolean>(false);
const modelName = ref<string>("");

const loadingModels = ref<boolean>(false);
const loadingModel = ref<boolean>(false);
const saving = ref<boolean>(false);

// Messages UI
const messageText = ref<string>("");
const messageType = ref<MessageType>("info");
const showMessageBox = ref<boolean>(false);

function showMessage(message: string, type: MessageType = "info") {
  messageText.value = message;
  messageType.value = type;
  showMessageBox.value = true;
  window.setTimeout(() => {
    showMessageBox.value = false;
  }, 5000);
}

// Dynamic form
const basicFields = ref<FieldDef[]>([]);
const advancedFields = ref<FieldDef[]>([]);
const formValues = ref<Record<string, any>>({});
// Computed property for model select options
const modelSelectOptions = computed(() => {
  if (loadingModels.value) {
    return [{ label: "Loading models...", value: "", disabled: true }];
  }

  if (availableModels.value.length === 0) {
    return [{ label: "No models available", value: "", disabled: true }];
  }

  return availableModels.value.map((model: any) => ({
    label: `${model.name} (${model.type})`,
    value: model.id,
    key: model.id,
  }));
});

const buttonText = computed<string>(() =>
  isCloning.value ? "Create New Model" : "Save Configuration"
);

const modelSelectPlaceholder = computed<string>(() => {
  if (loadingModel.value) return "Loading model...";
  if (loadingModels.value) return "Loading models...";
  return "Select a model...";
});

function onModelNameChange() {
  if (!selectedModel.value) return;
  const trimmedName = modelName.value.trim();
  isCloning.value = Boolean(
    trimmedName && trimmedName !== originalModelName.value
  );
}

function applyConfiguration(config: Record<string, any>) {
  Object.entries(config).forEach(([key, value]) => {
    if (key in formValues.value) {
      // Find the field to check its type
      const field = [...basicFields.value, ...advancedFields.value].find(
        (f) => f.name === key
      );
      if (field && field.type === "object") {
        formValues.value[key] = JSON.stringify(value, null, 2);
      } else {
        formValues.value[key] = value as any;
      }
    }
  });
}

function collectConfiguration(): Record<string, any> {
  const cfg: Record<string, any> = {};
  const all = [...basicFields.value, ...advancedFields.value];
  for (const field of all) {
    const val = formValues.value[field.name];
    if (field.type === "checkbox") {
      cfg[field.name] = Boolean(val);
    } else if (field.type === "number") {
      const num = typeof val === "number" ? val : parseFloat(String(val));
      cfg[field.name] = isNaN(num) ? undefined : num;
    } else if (field.type === "object") {
      try {
        cfg[field.name] = JSON.parse(val);
      } catch (e) {
        console.warn(`Failed to parse JSON for field ${field.name}:`, e);
        cfg[field.name] = val; // Keep as string if parsing fails
      }
    } else {
      cfg[field.name] = val;
    }
  }
  return cfg;
}

async function generateConfigForm(model: any) {
  let config: Record<string, any> = model.configuration || {};

  // Basic parameters to show first
  const basicParams = ["epochs", "batch_size", "learning_rate"];

  const toField = (key: string, value: any): FieldDef => {
    const fd: FieldDef = {
      name: key,
      label: key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
      default: value,
      type:
        typeof value === "boolean"
          ? "checkbox"
          : typeof value === "number"
          ? "number"
          : typeof value === "object" && value !== null
          ? "object"
          : "text",
    };
    return fd;
  };

  // Reset form state
  basicFields.value = [];
  advancedFields.value = [];
  formValues.value = {};

  // Generate form fields
  for (const [key, value] of Object.entries(config)) {
    const field = toField(key, value);

    if (field.type === "checkbox") {
      formValues.value[key] = Boolean(value);
    } else if (field.type === "object") {
      formValues.value[key] = JSON.stringify(value, null, 2);
    } else {
      formValues.value[key] = value;
    }

    if (basicParams.includes(key)) {
      basicFields.value.push(field);
    } else {
      advancedFields.value.push(field);
    }
  }
}

async function onModelSelected(modelId?: string) {
  // Handle both direct call and DlSelect event
  const id = modelId || selectedModelId.value;
  if (!id) {
    selectedModel.value = null;
    originalModelName.value = null;
    modelName.value = "";
    isCloning.value = false;
    basicFields.value = [];
    advancedFields.value = [];
    formValues.value = {};
    return;
  }

  loadingModel.value = true;

  try {
    let model = availableModels.value.find((m) => m.id === id);
    if (!model) {
      try {
        const response = await fetch(`${API_BASE}/models/${id}`);
        if (response.ok) model = await response.json();
      } catch (_) {}
    }

    if (model) {
      selectedModel.value = model;
      originalModelName.value = model.name;
      modelName.value = model.name || "";
      isCloning.value = false;
      await generateConfigForm(model);
      await nextTick();
      if (model.configuration && Object.keys(model.configuration).length > 0) {
        applyConfiguration(model.configuration);
        showMessage("Loaded existing model configuration", "success");
      }
    }
  } finally {
    loadingModel.value = false;
  }
}

async function loadModels() {
  loadingModels.value = true;
  availableModels.value = [];

  try {
    // Fetch models from API
    const url = `${API_BASE}/models?project_id=${currentProject.value.id}`;
    const response = await fetch(url);

    if (response.ok) {
      availableModels.value = await response.json();
    } else {
      const errorText = await response.text();
      console.error(`[Frontend] API Error: ${response.status} - ${errorText}`);
      availableModels.value = [];
    }

    // No fallback to defaults - keep empty if no models
    if (!availableModels.value || availableModels.value.length === 0) {
      console.log("[Frontend] No models available from backend");
      availableModels.value = [];
    }
  } catch (error) {
    console.error("[Frontend] Error loading models:", error);
    console.error("[Frontend] Error details:", {
      message: error.message,
      stack: error.stack,
    });
    // No defaults - keep empty on error
    availableModels.value = [];
  } finally {
    loadingModels.value = false;
  }
}

async function onSaveButtonClick() {
  const newModelName = modelName.value.trim();

  if (!newModelName) {
    showMessage("Please enter a model name", "error");
    return;
  }

  const config = collectConfiguration();
  saving.value = true;

  try {
    if (isCloning.value) {
      const response = await fetch(`${API_BASE}/models`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: newModelName,
          type: selectedModel.value.type,
          description: `Cloned from ${selectedModel.value.name}. ${selectedModel.value.description}`,
          configuration: config,
          base_model_id: selectedModel.value.id, // Important: include base model ID for cloning
          project_id: currentProject.value?.id,
        }),
      });

      if (response.ok) {
        const newModel = await response.json();
        console.log("[Frontend] New model created successfully:", newModel);
        showMessage("New model created successfully!", "success");

        // Update UI
        selectedModel.value = newModel;
        originalModelName.value = newModelName;
        isCloning.value = false;

        await loadModels();

        // Select the newly created model in the dropdown
        selectedModelId.value = newModel.id;
        // Refresh the form with the new model's configuration
        await onModelSelected();

        showMessage(
          `Model "${newModelName}" is now available in the dropdown!`,
          "success"
        );
      } else {
        const error = await response.json();
        showMessage(
          `Failed to create model: ${error.detail || "Unknown error"}`,
          "error"
        );
      }
    } else {
      // Update existing model
      const response = await fetch(
        `${API_BASE}/models/${selectedModel.value.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ configuration: config }),
        }
      );

      if (response.ok) {
        const updatedModel = await response.json();
        console.log(
          "[Frontend] Model configuration updated successfully:",
          updatedModel
        );

        // Update the selected model with the latest data
        selectedModel.value = updatedModel;

        // Refresh models list to get updated metadata
        await loadModels();

        // Select and reload the updated model to refresh the form
        selectedModelId.value = updatedModel.id;
        await onModelSelected();

        showMessage(
          `Model "${updatedModel.name}" configuration has been saved and reloaded!`,
          "success"
        );
      } else {
        const error = await response.json();
        console.error("[Frontend] Failed to save configuration:", error);
        showMessage(
          `Failed to save: ${error.detail || "Unknown error"}`,
          "error"
        );
      }
    }
  } catch (error) {
    showMessage("Failed to save: " + error.message, "error");
  } finally {
    saving.value = false;
  }
}

function cancel() {
  closeDialog();
}

function closeDialog() {
  if (window.dl && window.dl.agent) {
    window.dl.agent.sendEvent({
      name: "app:closeDialog",
      payload: { status: "closed" },
    });
  }
}

async function initialize() {
  try {
    // Get context from SDK

    const settings = await window.dl.settings.get();
    currentTheme.value = settings.theme;
    currentProject.value = await window.dl.projects.get();
    // Load models via API
    await loadModels();
  } catch (error) {
    showMessage("Initialization failed: " + error.message, "error");
  }
}

onMounted(() => {
  window.dl.on(DlEvent.READY, async () => {
    await initialize();
  });

  window.dl.on(DlEvent.THEME, (theme) => {
    currentTheme.value = theme;
  });
});

watch(modelName, onModelNameChange);
watch(currentTheme, (t) => {
  document.body.setAttribute(
    "data-theme",
    t === ThemeType.DARK ? "dark-mode" : "light-mode"
  );
});
</script>

<style>
/* Base Styles */
* {
  box-sizing: border-box;
}

body {
  background-color: var(--dl-color-bg);
  font-weight: 400;
  font-style: normal;
  font-family: "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  padding: 0;
  height: 100vh;
  overflow: hidden;
  color: var(--dl-color-darker);
}

#app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

#mainContent {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  padding-bottom: 100px;
  min-height: 0;
}

/* Typography */
h2 {
  font-size: var(--dl-font-size-h2);
  font-weight: 500;
  margin-bottom: 20px;
  color: var(--dl-color-darker);
}

h3 {
  font-size: var(--dl-font-size-h3);
  font-weight: 500;
  margin-bottom: 15px;
  color: var(--dl-color-darker);
}

label {
  font-size: var(--dl-font-size-h4);
  font-weight: 500;
  color: var(--dl-color-darker);
  display: block;
  margin-bottom: 5px;
}

/* Form Elements - inputs now using DlInput components */

/* Checkbox styles removed - now using DlCheckbox components */

/* Buttons - removed, now using DlButton components */

/* Sections */
section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: var(--dl-color-panel-background);
  border-radius: 8px;
  border: 1px solid var(--dl-color-separator);
}

/* Info/Message Boxes - Keep .info-box for model description */
.info-box {
  padding: 10px;
  background-color: var(--dl-color-info-background);
  border-radius: 4px;
  color: var(--dl-color-darker);
  margin-bottom: 10px;
  border: 1px solid var(--dl-color-info);
}

/* Custom padding for model description alert */
.margin-alert {
  margin-top: 5px;
  margin-bottom: 5px;
}

/* Form Groups */
.form-group {
  margin-bottom: 15px;
}

/* JSON Editor Wrapper */
.json-editor-wrapper {
  margin-bottom: 15px;
}

.json-editor-wrapper label {
  font-size: var(--dl-font-size-h4);
  font-weight: 500;
  color: var(--dl-color-darker);
  display: block;
  margin-bottom: 5px;
}

.json-editor-wrapper .json-editor {
  min-height: 150px;
  border: 1px solid var(--dl-color-separator);
  border-radius: 4px;
}

/* Actions Bar */
.actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background-color: var(--dl-color-panel-background);
  border-top: 1px solid var(--dl-color-separator);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.actions-left {
  display: flex;
  align-items: center;
}

.actions-right {
  display: flex;
  align-items: center;
}

/* Collapsible sections replaced with DlAccordion component */

/* Loading States */
.loading {
  color: var(--dl-color-medium);
  font-style: italic;
}

/* Utility Classes */
.hidden {
  display: none !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  #mainContent {
    padding: 15px;
  }

  .actions {
    flex-direction: column;
    gap: 10px;
  }

  .actions-left,
  .actions-right {
    width: 100%;
    justify-content: center;
  }

  .dl-button-container {
    margin: 5px;
  }
}
</style>
