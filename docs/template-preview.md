# AI Engineering MVP Template Preview

<div class="admonition note">
  <p class="admonition-title">Interactive Preview</p>
  <p>This page embeds the Vector Institute UI template. Click the button below to view the template UI.</p>
</div>

<div style="text-align: center; margin: 30px 0;">
  <a href="javascript:openTemplateUI()" class="md-button md-button--primary" style="background-color: #eb088a; color: white;">
    Open Template UI
  </a>
</div>

<iframe id="template-preview" src="" style="width: 100%; height: 600px; border: 1px solid #eee; border-radius: 5px; display: none;"></iframe>

<script>
function openTemplateUI() {
  // Get base URL - construct path to the template UI
  const baseUrl = window.location.origin + window.location.pathname.split('/').slice(0, -2).join('/');
  // Create template URL relative to the current page
  const templateUrl = baseUrl + '/assets/template-ui/';

  // Make iframe taller for better visibility
  document.getElementById('template-preview').style.height = '700px';

  // Option 1: Open in iframe
  document.getElementById('template-preview').src = templateUrl;
  document.getElementById('template-preview').style.display = 'block';

  // Option 2: Open in new tab
  // window.open(templateUrl, '_blank');
}
</script>

## About the Template UI

The AI Engineering MVP Template provides a clean, simple interface that adheres to Vector's branding guidelines:

- **Brand Colors**: Incorporates Vector's signature pink (#eb088a) and purple (#8a08eb)
- **Clean Design**: Minimalist interface with Vector branding
- **Responsive Layout**: Adapts to various screen sizes and devices

### How to Use

To use this template in your project:

1. Clone the repository
2. Navigate to the `frontend` directory
3. Install dependencies with `npm install`
4. Start the development server with `npm run dev`

For more details, see the [Frontend Development](frontend-development.md) documentation.
