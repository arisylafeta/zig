# 20250609154400_section_reordering

## Status: Completed

## Description
Currently, the StorySectionItem component doesn't provide the ability to reorder sections within a story. Users need the ability to move sections up and down to reorganize their stories without having to delete and recreate sections.

## Investigation
- The database schema already supports section ordering through the `order_index` column in the `story_sections` table
- The `sectionService.ts` already has an `updateSectionsOrder` function that can update the order of multiple sections at once
- The `StoryActionsContext` has a `handleMoveSections` function that could be used to implement this feature
- The `StorySectionItem` component currently lacks UI controls for moving sections up or down

## Requirements
1. Users should be able to reorder sections by clicking up/down buttons
2. The section order should be persisted to the database
3. The UI should provide appropriate feedback during reordering operations
4. Edge cases should be handled properly (e.g., can't move first section up or last section down)

## Implementation Plan
1. Update the StorySectionItem component to add up/down buttons in the card footer:
   ```tsx
   <div className="flex items-center space-x-2">
     <Button
       variant="outline"
       size="sm"
       onClick={() => onMoveSection('up')}
       disabled={index === 0}
       className="flex items-center space-x-1"
     >
       <ArrowUp className="h-4 w-4" />
       <span className="sr-only">Move Up</span>
     </Button>
     <Button
       variant="outline"
       size="sm"
       onClick={() => onMoveSection('down')}
       disabled={index === totalSections - 1}
       className="flex items-center space-x-1"
     >
       <ArrowDown className="h-4 w-4" />
       <span className="sr-only">Move Down</span>
     </Button>
   </div>
   ```

2. Update the StorySectionItem props interface to include the new callback and totalSections count:
   ```tsx
   interface StorySectionItemProps {
     section: StorySection;
     index: number;
     isPreviewing: boolean;
     onChangeLayout: () => void;
     onTogglePreview: () => void;
     onDelete: () => void;
     onUpdate: (updatedSection: StorySection) => void;
     onMoveSection?: (direction: 'up' | 'down') => void; // New prop, optional
     totalSections: number; // New prop to handle edge cases
   }
   ```

3. Implement the section reordering logic in the parent component (StoryCreationView):
   ```tsx
   const handleMoveSection = (index: number, direction: 'up' | 'down') => {
     if (
       (direction === 'up' && index === 0) || 
       (direction === 'down' && index === sections.length - 1)
     ) {
       return; // Can't move first section up or last section down
     }
     
     const newSections = [...sections];
     const targetIndex = direction === 'up' ? index - 1 : index + 1;
     
     // Swap the sections
     [newSections[index], newSections[targetIndex]] = [newSections[targetIndex], newSections[index]];
     
     // Update the order_index values
     const updatedSections = newSections.map((section, idx) => ({
       ...section,
       order_index: idx
     }));
     
     // Use the existing context function to update the sections
     storyActions.handleMoveSections(updatedSections);
   };
   ```

4. Update the StorySections component to pass the onMoveSection callback and totalSections to each StorySectionItem:
   ```tsx
   <StorySectionItem
     section={section}
     index={index}
     isPreviewing={previewingSections[section.id] || false}
     onChangeLayout={() => onChangeLayout(index)}
     onTogglePreview={() => onTogglePreview(section.id)}
     onDelete={() => onDeleteSection(index)}
     onUpdate={(updatedSection) => onUpdateSection(index, updatedSection)}
     onMoveSection={onMoveSection ? (direction) => onMoveSection(index, direction) : undefined}
     totalSections={sections.length}
   />
   ```

5. Update the handleMoveSections function in StoryActionsProvider to persist changes to the database and invalidate caches:
   ```tsx
   const handleMoveSections = async (newSections: StorySection[]) => {
     // Update local state immediately for a responsive UI
     setSections(newSections);
     
     try {
       // Prepare the data for the API call
       const updates = newSections.map((section, index) => ({
         id: section.id,
         order_index: index
       }));
       
       // Persist the changes to the database
       const success = await sectionService.updateSectionsOrder(updates);
       
       if (!success) {
         throw new Error('Failed to update sections order');
       }
       
       // Invalidate all relevant queries to ensure we get fresh data everywhere
       queryClient.invalidateQueries({ queryKey: ['story'] });
       queryClient.invalidateQueries({ queryKey: ['stories'] });
       queryClient.invalidateQueries({ queryKey: ['sections'] });
       
       // Force refetch the current story to update local state
       if (currentStory?.id) {
         await queryClient.refetchQueries({ queryKey: ['story', currentStory.id], type: 'active' });
       }
       
       toast({
         title: "Success",
         description: "Section order updated successfully",
         variant: "default"
       });
     } catch (error) {
       console.error('Error persisting section order:', error);
       toast({
         title: "Error",
         description: "Failed to save section order. Please try again.",
         variant: "destructive"
       });
     }
   };
   ```

6. Replace the unimplemented RPC function in sectionService with direct database updates:
   ```tsx
   async updateSectionsOrder(sections: { id: string, order_index: number }[]): Promise<boolean> {
     try {
       // First, get the story_id from one of the sections to update the parent story timestamp later
       let storyId: string | null = null;
       if (sections.length > 0) {
         const { data: sectionData, error: fetchError } = await supabase
           .from('story_sections')
           .select('story_id')
           .eq('id', sections[0].id)
           .single();
         
         if (fetchError) {
           console.error(`Error fetching story_id for section ${sections[0].id}:`, fetchError);
         } else if (sectionData) {
           storyId = sectionData.story_id;
         }
       }
       
       // Update each section's order_index individually
       // We can't use a bulk update because each section needs a different order_index value
       for (const section of sections) {
         const { error } = await supabase
           .from('story_sections')
           .update({ order_index: section.order_index })
           .eq('id', section.id);
         
         if (error) {
           console.error(`Error updating order for section ${section.id}:`, error);
           throw error;
         }
       }
       
       // Update the parent story's timestamp if we have the story_id
       if (storyId) {
         await this.updateParentStoryTimestamp(storyId);
       }
       
       return true;
     } catch (error) {
       console.error("Error updating sections order:", error);
       toast.error("Failed to update sections order");
       return false;
     }
   }
   ```

7. Fix the updateParentStoryTimestamp function to avoid 406 errors:
   ```tsx
   async updateParentStoryTimestamp(storyId: string): Promise<void> {
     try {
       // First, check if the story exists
       const { data, error } = await supabase
         .from('stories')
         .select('id')
         .eq('id', storyId)
         .maybeSingle();
       
       if (error) {
         console.error(`Error checking if story ${storyId} exists:`, error);
         return;
       }
       
       if (!data) {
         console.error(`Story ${storyId} not found, cannot update timestamp`);
         return;
       }
       
       // Use a dummy update that doesn't change any visible data
       // but will trigger Postgres to update the updated_at timestamp
       const { error: updateError } = await supabase
         .from('stories')
         .update({ id: storyId })
         .eq('id', storyId);
       
       if (updateError) {
         console.error(`Error updating timestamp for story ${storyId}:`, updateError);
       }
     } catch (error) {
       console.error(`Error updating parent story timestamp for story ${storyId}:`, error);
     }
   }
   ```

8. Update the deleteSection function to reindex remaining sections after deletion:
   ```tsx
   // After deleting a section, get all remaining sections and update their order_index values
   const { data: remainingSections, error: fetchSectionsError } = await supabase
     .from('story_sections')
     .select('id, order_index')
     .eq('story_id', storyId)
     .order('order_index', { ascending: true });
   
   if (fetchSectionsError) {
     console.error(`Error fetching remaining sections for story ${storyId}:`, fetchSectionsError);
   } else if (remainingSections && remainingSections.length > 0) {
     // Update the order_index for all sections that were after the deleted one
     const sectionsToUpdate = remainingSections
       .filter(section => section.order_index > deletedSectionIndex)
       .map(section => ({
         id: section.id,
         order_index: section.order_index - 1 // Decrease the index by 1
       }));
     
     if (sectionsToUpdate.length > 0) {
       // Update each section's order_index
       for (const section of sectionsToUpdate) {
         await supabase
           .from('story_sections')
           .update({ order_index: section.order_index })
           .eq('id', section.id);
       }
     }
   }
   ```

9. Add sorting to ensure sections are displayed in the correct order:
   ```tsx
   // In transformStoryForUI function
   const sortedSections = [...story.story_sections].sort((a, b) => {
     // Sort by order_index
     if (a.order_index !== undefined && b.order_index !== undefined) {
       return a.order_index - b.order_index;
     }
     return 0;
   });
   ```

## Completed Implementation

- ✅ Added up/down arrow buttons to StorySectionItem component
- ✅ Implemented section reordering via drag-and-drop and arrow buttons
- ✅ Fixed the backend persistence by replacing the unimplemented RPC with direct database updates
- ✅ Added proper React Query cache invalidation to ensure UI reflects the latest order
- ✅ Fixed the updateParentStoryTimestamp function to avoid 406 errors
- ✅ Added reindexing of sections after deletion to maintain continuous ordering
- ✅ Added sorting in the transformStoryForUI function to ensure consistent display order

## Known Issues and Future Improvements

- When navigating to the edit page via StoryCard, the sections may initially load in incorrect order until page refresh
- The 406 error may still occur in some edge cases when updating stories
- Consider adding loading indicators during section reordering operations
