# ConvNeXt — One-Page Notes
*"A ConvNet for the 2020s" — Liu et al., 2022 (Facebook AI Research)*

## What it is
A pure ConvNet, modernized by systematically borrowing design choices from Vision Transformers (especially Swin), starting from a ResNet-50 and applying changes one at a time. No attention, no patches-as-tokens — just convolutions, redesigned.

## The Roadmap (cumulative accuracy on ImageNet-1K)
| Stage | Change | Top-1 |
|---|---|---|
| 0 | ResNet-50 baseline | 76.1% |
| 1 | **Modern training recipe** (300 epochs, AdamW, Mixup/CutMix/RandAugment, stochastic depth, label smoothing) — no architecture change | 78.8% |
| 2 | Macro design: stage ratio 3:4:6:3 → 3:3:9:3, "patchify" stem (4×4 stride-4 conv) | ~79.5% |
| 3 | ResNeXt-ify: grouped/depthwise conv + width increase | ~80.5% |
| 4 | **Inverted bottleneck** (narrow→wide→narrow, like MobileNetV2 / Transformer MLP) | 80.6% (temporarily 79.9% right after moving depthwise conv up) |
| 5 | **Large kernel** (move depthwise conv up in block, 3×3 → 7×7) | 80.6% |
| 6 | Micro design: ReLU→GELU, fewer activations (1 per block), fewer norms (1 per block), BatchNorm→LayerNorm, separate downsampling layers | **82.1%** |

**Total gain: +6.0%** → roughly **+2.7% from training recipe**, **+3.3% from architecture**.

## Key architectural ideas

**Inverted bottleneck** (borrowed from MobileNetV2):
- ResNet bottleneck: wide → narrow → wide (256→64→64→256), standard 3×3 conv in the middle
- ConvNeXt block: narrow → wide → narrow (96→384→96), **depthwise** 7×7 conv at input width
- Mimics a Transformer block: spatial mixing (like attention) → wide MLP-style channel mixing

**Depthwise separable convolution** — the real compute-saving trick:
- Standard conv FLOPs: `H×W × C_in × C_out × K²`
- Depthwise conv FLOPs: `H×W × C × K²` (no cross-channel term)
- Makes a large 7×7 kernel ~96× cheaper than a standard 7×7 at the same channel count — this is what lets ConvNeXt afford a big receptive field (ViT-style) without exploding compute.

**Micro design** (Transformer-style layer choices):
- 1 normalization layer per block (not 3) — placed before the first 1×1 conv
- 1 activation per block (GELU, not ReLU) — placed between the two 1×1 convs
- BatchNorm → LayerNorm

## Common misconception (worth remembering)
ConvNeXt blocks are **not** individually cheaper than ResNet blocks at matched channel width — an inverted-bottleneck block with 4× expansion actually costs *more* FLOPs per block than a ResNet bottleneck at the same width. The efficiency gain comes from:
1. Depthwise convs making large kernels cheap (real saving)
2. **Network-level tuning** — ConvNeXt uses narrower base channel widths per stage than ResNet, so total-network FLOPs land close to ResNet's (ConvNeXt-T: 4.5 GFLOPs vs ResNet-50: 4.1 GFLOPs — matched, not lower)

So the real story: **better accuracy per FLOP**, not fewer FLOPs overall.

## What the paper does *not* claim
- No memory or latency numbers are reported for individual micro-design changes (e.g., "fewer norm layers") — only accuracy deltas in the ablation table.
- Final throughput comparisons (ConvNeXt vs Swin vs ResNet on A100 GPUs) are reported only for the complete final models, as an aggregate effect of all changes combined.

## Final numbers
| Model | GFLOPs | Params | Top-1 |
|---|---|---|---|
| ResNet-50 | 4.1 | 25.6M | 76.1% |
| ConvNeXt-T | 4.5 | 28.6M | 82.1% |
| ResNet-200 | 15.0 | 64.7M | 78.2% |
| ConvNeXt-B | 15.4 | 89M | 83.8% |
