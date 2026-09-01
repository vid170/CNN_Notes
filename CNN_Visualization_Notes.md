# CNN Visualization Methods — Concise Notes

All methods below are **"don't disturb the model"** methods — the trained CNN itself is never modified, we only probe it to understand what it learned.

## 1. Visualizing Filters/Kernels Directly
- A filter is just a small matrix → can be plotted as an image (e.g., AlexNet: 64 filters, 11×11×3 in conv1).
- **First-layer filters** are interpretable: edge detectors (various orientations), checkerboard/striation patterns, color-blob/color-edge detectors.
- This pattern is **consistent across models** (AlexNet, ResNet-18/101, DenseNet-121) → called **"Gabor-like filter fatigue"** (Gabor = Gaussian × sinusoid; same edge/orientation/scale detection the CNN learns on its own).
- **Higher-layer filters are NOT interpretable this way** — inputs to deeper layers aren't raw images anymore, and with many diverse classes (e.g., ImageNet's 1000 classes) the abstractions don't visually "make sense" as plotted weights.
  - Also, learned representations at higher layers **aren't generic anymore** — since the dataset has a wide variety of classes/objects, the specialized features learned end up being just as varied/diverse, so there's no single consistent visual pattern to point to (unlike the universal edge/blob detectors at layer 1).
  - (Works better only in narrow domains, e.g., faces → eyes/nose → whole face, where the range of specialized features is limited enough to make visual sense.)

![First-layer filters across AlexNet, ResNet-18, ResNet-101, DenseNet-121](images/filters_visualization.jpg)
*First-layer filters look nearly identical (Gabor-like) across very different architectures — AlexNet, ResNet, DenseNet.*

## 2. Visualizing the Representation Space (Embeddings)
- Take the penultimate FC layer output (e.g., AlexNet FC7 = 4096-dim vector) for many images.
- Reduce dimensionality (PCA, or better: **t-SNE** — t-distributed Stochastic Neighbor Embedding, Hinton & van der Maaten, 2008) down to 2D and plot.
- **Result**: images of the same class cluster together (shown clearly on MNIST); on ImageNet, semantically similar images (e.g., all cars, all fields) group together.
- **Insight**: CNN representations capture *semantics* — unlike hand-crafted features (SIFT/HOG/LBP) which require manual design, the CNN learns useful representations automatically. This is also why a simple classifier on top of the penultimate layer works well.

![t-SNE reducing FC7 4096-dim vectors to 2D, forming clusters](images/tsne_representation_space.jpg)
*FC7 (4096-dim) features reduced to 2D via t-SNE — same-class images cluster together (inset shows labeled clusters, e.g. on MNIST).*

![t-SNE map on ImageNet showing images placed by embedding location](images/tsne_zoomed_clusters.jpg)
*Zoomed-in region of an ImageNet t-SNE map — images that are nearby in this space (e.g., all "fields," circled in red) are semantically similar to the CNN.*

## 3. Visualizing Feature Maps / Maximally Activating Patches
- Feature maps of a layer (e.g., AlexNet conv5: 128 × 13×13) can be visualized as grayscale images — can reveal higher-level semantics (e.g., one map capturing "two people" in an image).
- **Neuron activation approach**: pick a single neuron in an intermediate layer → find which input images/patches make it fire most → trace back through **receptive fields** (layer by layer) to see which region of the original image is responsible.
- Result: different neurons specialize — e.g., one fires for human busts, another for dogs, another for a red blob, another for digits, another for specular reflections.
- **Connects to Dropout**: training encourages diverse neurons rather than all overfitting to the same pattern.

![Tracing a single neuron back through the CNN to its receptive field in the input image](images/activating_patches_concept.jpg)
*Pick one neuron in an intermediate layer → feed images → trace back the receptive field to find which input patch caused it to fire.*

![Grid of maximally activating patches — each row = one neuron, showing what it specializes in](images/activating_patches_grid.jpg)
*Each row shows the patches that maximally activate one specific neuron — e.g., people, dogs, honeycomb/flag patterns, text, or specular highlights.*

## 4. Occlusion Experiments
- Goal: find out **which pixels/regions** actually drove the CNN's prediction (did it look at the cat, or just the grass background?).
- Method: slide a gray occlusion patch across the image; for each position, run the occluded image through the CNN and record the predicted probability of the correct class (softmax output).
- Plot all probabilities as a **heat map** (red = high prob, blue = low prob).
- **Result**: probability drops sharply when the patch covers the actually relevant object (e.g., dog's face for "Pomeranian", wheel for "car wheel", dog for "Afghan Hound" even amid humans in the image).
- Source: Zeiler & Fergus, *"Visualizing and Understanding Convolutional Neural Networks."*
- Practical value: builds trust that the model is learning the right correlations, not spurious ones (e.g., "cat" ≠ "grass background").

![Occlusion heat maps — Pomeranian, car wheel, Afghan Hound examples](images/occlusion_experiments.jpg)
*Sliding a gray patch over the image and plotting predicted probability at each position — the probability drops (blue) exactly where the relevant object (dog's face, wheel) is occluded, confirming the CNN is looking at the right region.*

## Summary Table

| Method | What it shows | Limitation |
|---|---|---|
| Filter visualization | Low-level features (edges, color blobs) — Gabor-like, consistent across models | Only interpretable at layer 1 |
| Representation space (t-SNE) | Semantic clustering of classes in embedding space | Needs dimensionality reduction, only qualitative |
| Max-activating patches / feature maps | What patterns/objects each neuron specializes in | Requires tracing receptive fields back to input |
| Occlusion experiments | Which image region drives the final prediction | Computationally expensive (slide patch over entire image) |

**Further reading/tools**: CS231n Lecture 13 notes, Jason Yosinski's Deep Visualization Toolkit (demo video), t-SNE resources, Zeiler & Fergus (2014) paper.
