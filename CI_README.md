# GitLab CI/CD Pipeline Documentation

## Overview

This project uses GitLab CI/CD to automatically run agent tests whenever code changes are pushed to the repository.

## Pipeline Triggers

The pipeline is configured to run automatically on:

1. **Push to main branch** - Every commit pushed to the `main` branch
2. **Merge Requests (Pull Requests)** - All merge requests targeting any branch
3. **Manual runs** - Can be triggered manually from the GitLab UI

## Tests Executed

The pipeline runs three test suites in sequence:

### 1. Game Smoke Tests (`game_smoke_test.py`)
- **Purpose**: Quick sanity checks to ensure agents can play games
- **Tests**:
  - ValueIterationAgent plays one game and finishes
  - PolicyIterationAgent plays one game and finishes
  - QLearningAgent plays one game and finishes
- **Duration**: Fast (~1-2 minutes)

### 2. Convergence Tests (`convergence_test.py`)
- **Purpose**: Verify that agents converge to stable policies
- **Tests**:
  - ValueIteration produces stable results across multiple evaluations
  - PolicyIteration produces stable results across multiple evaluations
  - QLearning improves or maintains performance with additional training
- **Duration**: Medium (~5-10 minutes)

### 3. Policy Quality Tests (`test_q_learning.py`)
- **Purpose**: Ensure trained agents outperform random baseline
- **Tests**:
  - ValueIterationAgent outperforms random agent
  - PolicyIterationAgent outperforms random agent
  - QLearningAgent outperforms random agent
- **Duration**: Long (~10-15 minutes)

## Pipeline Configuration

### Docker Image
- **Base Image**: `python:3.9`
- Provides a clean Python 3.9 environment for testing

### Dependencies
All dependencies are installed from `requirements.txt`:
- `Pillow` - Image processing for game visualization
- `pytest` - Testing framework
- `pytest-timeout` - Timeout support for long-running tests

### Caching
Pip packages are cached between pipeline runs to speed up execution:
- Cache key is based on `requirements.txt` content
- Cache is stored in `.cache/pip` directory

### Artifacts
Test results are collected and stored as artifacts:
- **Format**: JUnit XML (for GitLab test reporting)
- **Retention**: 1 week
- **Collection**: Always (even on failure)

## Viewing Pipeline Results

### In GitLab UI
1. Navigate to **CI/CD > Pipelines** in your GitLab project
2. Click on a pipeline to see the job status
3. Click on the `test:all-agents` job to view logs
4. View test results in the **Tests** tab

### Pipeline Status Badge
Add this to your README.md to show pipeline status:
```markdown
[![Pipeline Status](https://gitlab.com/<your-username>/<your-project>/badges/main/pipeline.svg)](https://gitlab.com/<your-username>/<your-project>/-/pipelines)
```

## Running Tests Locally

To run the same tests locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest src/pacman/controllers/agents/game_smoke_test.py -v
pytest src/pacman/controllers/agents/convergence_test.py -v
pytest src/pacman/controllers/agents/test_q_learning.py -v

# Or run all at once
pytest src/pacman/controllers/agents/ -v
```

## Customization Options

### Modify Test Execution
Edit `.gitlab-ci.yml` to:
- Add more test files
- Change Python version (modify `image: python:3.9`)
- Add parallel test execution
- Configure test timeouts

### Add Code Quality Checks
You can extend the pipeline with additional stages:
```yaml
stages:
  - lint
  - test
  - deploy

lint:
  stage: lint
  script:
    - pip install flake8 black
    - flake8 src/
    - black --check src/
```

### Optimize for Specific Changes
To run tests only when agent code changes, add this to the job:
```yaml
test:all-agents:
  only:
    changes:
      - src/pacman/controllers/agents/**/*
      - src/pacman/**/*.py
```

## Troubleshooting

### Pipeline Fails with Import Errors
- Ensure all dependencies are listed in `requirements.txt`
- Check that the Python path is correctly set in test files

### Tests Timeout
- Increase timeout in `.gitlab-ci.yml`:
  ```yaml
  script:
    - python -m pytest --timeout=300 src/pacman/controllers/agents/
  ```

### Cache Issues
- Clear the cache in GitLab UI: **CI/CD > Pipelines > Clear Runner Caches**

## Best Practices

1. **Always run tests locally** before pushing to catch issues early
2. **Keep tests fast** - Slow tests discourage frequent commits
3. **Fix failing tests immediately** - Don't let them accumulate
4. **Review test output** in merge requests before merging
5. **Update tests** when adding new agents or changing behavior

## Support

For issues with the CI/CD pipeline:
1. Check the pipeline logs in GitLab
2. Verify `.gitlab-ci.yml` syntax using GitLab's CI Lint tool
3. Ensure all test files are committed to the repository
