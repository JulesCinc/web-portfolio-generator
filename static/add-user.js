
(function() {
  /**
   * Counter for unique ID for the projects
   */
  let projectCounter = 0;

  /**
   * Add project bloc
   */
  function addProjectBlock(container) {
    projectCounter++;
    const projectId = `project-${projectCounter}`;
    
    const projectHTML = `
      <fieldset id="${projectId}" class="project-block">
        <legend>Project #${projectCounter}</legend>
        <button type="button" class="remove-project-btn" data-project-id="${projectId}">
           Delete project
        </button>
        
        <p>
          <label for="${projectId}-name">Project name * :</label>
          <input type="text" id="${projectId}-name" name="project-name-${projectCounter}" required />
        </p>
        
        <p>
          <label for="${projectId}-description">Description * :</label>
          <textarea id="${projectId}-description" name="project-description-${projectCounter}" required></textarea>
        </p>
        
        <p>
          <label for="${projectId}-image">Image (URL) :</label>
          <input type="url" id="${projectId}-image" name="project-image-${projectCounter}" placeholder="https://..." />
        </p>
        
        <p>
          <label for="${projectId}-link">Link :</label>
          <input type="url" id="${projectId}-link" name="project-link-${projectCounter}" placeholder="https://..." />
        </p>
        
        <p>
          <label for="${projectId}-dotlist">Dotlist (coma separated) :</label>
          <input type="text" id="${projectId}-dotlist" name="project-dotlist-${projectCounter}" placeholder="Item1, Item2, Item3" />
        </p>
      </fieldset>
    `;
    
    container.insertAdjacentHTML('beforeend', projectHTML);
    
    // Add 'delete project' event
    const removeBtn = document.getElementById(projectId).querySelector('.remove-project-btn');
    if (removeBtn) {
      removeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const projectBlock = document.getElementById(this.dataset.projectId);
        if (projectBlock) {
          projectBlock.remove();
          console.log(`Project deleted`);
        }
      });
    }
  }


  /**
   * Setup form
   */
  function setupAddUserForm() {
    const form = document.getElementById("add-user-form");
    const addProjectBtn = document.getElementById("add-project-btn");
    const projectsContainer = document.getElementById("projects-container");

    // Ensure elements exist
    if (!form || !addProjectBtn || !projectsContainer) {
      console.log("Error: form's element don't exist");
      return;
    }

    console.log("Forms added");

    // Add a project block by default
    addProjectBlock(projectsContainer);

    // Event to add new blocks
    addProjectBtn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      addProjectBlock(projectsContainer);
    });

    // Avoid double submission
    let isSubmitting = false;

    // Submit event
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      e.stopPropagation();

      // Avoid double submission
      if (isSubmitting) {
        console.log("Already submitting");
        return;
      }

      isSubmitting = true;
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Creating...";
      }

      try {
        // 1. Get user data
        const userData = {
          name: document.getElementById("name")?.value || "",
          firstname: document.getElementById("firstname")?.value || "",
          age: parseInt(document.getElementById("age")?.value) || 0,
          email: document.getElementById("email")?.value || "",
          github: document.getElementById("github")?.value || null,
          tel: document.getElementById("tel")?.value || null
        };

        // Check non NULL
        if (!userData.name || !userData.firstname || !userData.email || !userData.age) {
          alert("Please, fill mandatory fields");
          throw new Error("Mandatory field missing");
        }

        console.log("Send User :", userData);

        // 2. Create User
        const userResponse = await fetch("/add_user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (!userResponse.ok) {
          throw new Error(`Error: can't create user: (${userResponse.status})`);
        }

        const newUser = await userResponse.json();
        console.log("User created :", newUser);

        // 3. Get and create projects
        const projectBlocks = document.querySelectorAll('.project-block');
        const projects = [];

        projectBlocks.forEach(block => {
          const nameInput = block.querySelector('input[id$="-name"]');
          const descriptionInput = block.querySelector('textarea[id$="-description"]');

          // Create only project with name and description
          if (nameInput && descriptionInput && nameInput.value && descriptionInput.value) {
            const project = {
              user_id: newUser.user_id,
              name: nameInput.value,
              description: descriptionInput.value,
              image_path: block.querySelector('input[id$="-image"]')?.value || null,
              link: block.querySelector('input[id$="-link"]')?.value || null,
              dotlist: block.querySelector('input[id$="-dotlist"]')?.value || null
            };
            projects.push(project);
          }
        });

        console.log(` Submitting ${projects.length} project(s)`);

        // Create all projects in //
        if (projects.length > 0) {
          const projectPromises = projects.map(project =>
            fetch("/add_project", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(project),
            }).then(response => {
              if (!response.ok) {
                throw new Error(`Error, can't create project: ${project.name}`);
              }
              return response.json();
            })
          );

          await Promise.all(projectPromises);
          console.log(`${projects.length} project(s) created`);
        }

        // 4. Sucess message
        const message = `✅ User "${newUser.name} ${newUser.firstname}" created ${projects.length > 0 ? ' and ' + projects.length + ' project(s) created' : ''} !`;
        alert(message);

        // 5. Redirect to base page
        setTimeout(() => {
          window.location.href = "/";
        }, 500);

      } catch (error) {
        console.error("❌ Error :", error);
        alert(`❌ Error : ${error.message}`);
      } finally {
        // Reactivate submit button
        isSubmitting = false;
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = "Create user and projects";
        }
      }
    });
  }

  // Initialisation au chargement de la page
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupAddUserForm);
  } else {
    setupAddUserForm();
  }
})();
